package com.chess.gameservice.game.board;

import com.chess.gameservice.exception.GameException;
import com.chess.gameservice.game.graveyard.Graveyards;
import com.chess.gameservice.game.piece.*;
import com.chess.gameservice.game.player.PlayerColor;
import com.chess.gameservice.game.position.Position;
import com.fasterxml.jackson.annotation.JsonIgnore;
import lombok.EqualsAndHashCode;
import lombok.Getter;
import lombok.Setter;

import java.io.*;
import java.util.ArrayList;
import java.util.EnumMap;

@Getter
@Setter
@EqualsAndHashCode
public class Board implements Serializable{
    @JsonIgnore
    public static final int BOARD_SIZE = 7;
    @JsonIgnore
    public static final int BOTTOM_ROW = 0;
    @JsonIgnore
    private final PieceType[][] playerInitialState =
            {{PieceType.PAWN, PieceType.PAWN, PieceType.PAWN, PieceType.PAWN,
                    PieceType.PAWN, PieceType.PAWN, PieceType.PAWN, PieceType.PAWN},
                    {PieceType.ROOK, PieceType.KNIGHT, PieceType.BISHOP, PieceType.QUEEN,
                            PieceType.KING, PieceType.BISHOP, PieceType.KNIGHT, PieceType.ROOK}};

    private Graveyards graveyards;
    Position positionAwaitingPromotion;
    private Piece[][] state;
    private CheckState checkState;
    private EnumMap<PlayerColor, Position> kingPositions = new EnumMap<>(PlayerColor.class);

    @JsonIgnore
    Position enPessantPosition;
    
    private Integer halfMoveClock = 0;
    private Integer fullMoveNumber = 1;

    public Board() {
        graveyards = new Graveyards();
        state = new Piece[BOARD_SIZE + 1][BOARD_SIZE + 1];
        checkState = CheckState.NONE;
        populateBoard();
    }

    public Board deepCopy() throws IOException, ClassNotFoundException {
        ByteArrayOutputStream baos = new ByteArrayOutputStream();
        ObjectOutputStream oos = new ObjectOutputStream(baos);
        oos.writeObject(this);

        ByteArrayInputStream bais = new ByteArrayInputStream(baos.toByteArray());
        ObjectInputStream ois = new ObjectInputStream(bais);
        return (Board) ois.readObject();
    }

    private void populateBoard() {
        populateWhite();
        populateBlack();
        setKingPosition(PlayerColor.BLACK, new Position(0, 4));
        setKingPosition(PlayerColor.WHITE, new Position(7, 4));
    }

    public void setKingPosition(PlayerColor kingColor, Position position) {
        kingPositions.put(kingColor, position);
    }

    public Position getKingPosition(PlayerColor kingColor) {
        return kingPositions.get(kingColor);
    }

    private void populateWhite() {
        int z = 0;
        for (int x = 6; x <= BOARD_SIZE; x++) {
            for (int y = 0; y <= BOARD_SIZE; y++) {
                state[x][y] = PieceFactory.buildPiece(playerInitialState[z][y], PlayerColor.WHITE);
            }
            z++;
        }
    }

    private void populateBlack() {
        for (int x = 1; x >= 0; x--) {
            for (int y = BOARD_SIZE; y >= 0; y--) {
                state[1 - x][y] = PieceFactory.buildPiece(playerInitialState[x][y], PlayerColor.BLACK);
            }
        }
    }

    public void setBoardPosition(Position position, Piece piece) {
        state[position.getX()][position.getY()] = piece;
    }

    public Piece getPieceByPosition(Position position) {
        return state[position.getX()][position.getY()];
    }

    public boolean isBoardPositionEmpty(Position position) {
        return state[position.getX()][position.getY()] == null;
    }

    public boolean isTakenPositionMovable(Position initialPosition, PlayerColor playerColor) {
        if (isBoardPositionEmpty(initialPosition)) {
            return true;
        }
        return isPositionTakenByEnemy(initialPosition, playerColor);
    }

    public boolean isPositionAttackable(Position initialPosition, PlayerColor playerColor) {
        return !isBoardPositionEmpty(initialPosition) && isPositionTakenByEnemy(initialPosition, playerColor);
    }

    public boolean isPositionTakenByAttackableEnemy(Position initialPosition, PlayerColor playerColor) {
        return !isBoardPositionEmpty(initialPosition) && isPositionTakenByEnemy(initialPosition, playerColor) && isEnemyAttackable(initialPosition);
    }

    private boolean isPositionTakenByEnemy(Position initialPosition, PlayerColor playerColor) {
        return getPieceByPosition(initialPosition).getPlayerColor() != playerColor;
    }

    private boolean isEnemyAttackable(Position initialPosition) {
        return !(getPieceByPosition(initialPosition) instanceof King);
    }


    public ArrayList<Position> getAvailableMoves(Position position, PlayerColor playerColor) throws GameException {
        var piece = getPieceByPosition(position);

        if (piece == null) {
            throw new GameException("No piece selected.");
        }

        if (piece.getPlayerColor() != playerColor) {
            throw new GameException("Wrong piece color.");
        }

        return piece.getAvailableMoves(this, position);
    }

    public Piece movePiece(Position initialPosition, Position destination, PlayerColor playerColor) throws GameException {
        var piece = getPieceByPosition(initialPosition);

        if (piece == null) {
            throw new GameException("No piece selected.");
        }

        if (piece.getPlayerColor() != playerColor) {
            throw new GameException("Invalid piece color.");
        }

        if (piece.isMoveImpossible(initialPosition, destination)) {
            throw new GameException("Illegal move.");
        }

        if (!isTakenPositionMovable(destination, piece.getPlayerColor())) {
            throw new GameException("Illegal move.");
        }

        if (!piece.isMoveLegal(initialPosition, destination, this)) {
            throw new GameException("Illegal move.");
        }

        if (CheckChecker.willMoveResultInCheck(this, initialPosition, destination)) {
            throw new GameException("Move ends with check.");
        }

        addPieceToGraveyardByPosition(destination);

        // update en passant position
        if (piece instanceof Pawn) {
            if (Math.abs(initialPosition.getX() - destination.getX()) == 2) {
                enPessantPosition = new Position((initialPosition.getX() + destination.getX()) / 2, initialPosition.getY());
            } else {
                enPessantPosition = null;
            }
        } else {
            enPessantPosition = null;
        }
        // update half move clock
        if (piece instanceof Pawn || !isBoardPositionEmpty(destination)) {
            halfMoveClock = 0; // reset because of pawn move or capture
        } else {
            halfMoveClock++;
        }
        // update full move number
        if (piece.getPlayerColor() == PlayerColor.BLACK) {
            fullMoveNumber++;
        }

        piece.makeMove(initialPosition, destination, this);
        setCheckState(CheckChecker.getCheckState(this, PlayerColor.getOtherColor(piece.getPlayerColor())));
        return piece;
    }

    public void addPieceToGraveyardByPosition(Position position) {
        Piece removedPiece = getPieceByPosition(position);

        if (removedPiece != null) {
            graveyards.addPieceToCorrectGraveyard(removedPiece);
        }
    }

    public void makePromotion(Position position, PlayerColor playerColor, PieceType selectedPromotion) throws GameException {
        Piece piece = getPieceByPosition(position);
        Piece promotedPiece = PieceFactory.buildPiece(selectedPromotion, playerColor);

        if (positionAwaitingPromotion == null) {
            throw new GameException("No pawn awaiting promotion.");
        }
        if (!(piece instanceof Pawn)) {
            throw new GameException("Piece is not a pawn.");
        }
        if (playerColor != piece.getPlayerColor()) {
            throw new GameException("Invalid pawn color.");
        }
        if (promotedPiece instanceof Pawn) {
            throw new GameException("Invalid piece type.");
        }

        setBoardPosition(position, promotedPiece);
        positionAwaitingPromotion = null;
        setCheckState(CheckChecker.getCheckState(this, PlayerColor.getOtherColor(piece.getPlayerColor())));
    }

    public boolean whiteCanCastleKingSide() {
        // check if the king and rook have not moved
        Piece king = getPieceByPosition(new Position(7, 4));
        Piece rook = getPieceByPosition(new Position(7, 7));
        return king != null && rook != null && king.getPlayerColor() == PlayerColor.WHITE && rook.getPlayerColor() == PlayerColor.WHITE &&
                king.isFirstMove() && rook.isFirstMove();
    }

    public boolean whiteCanCastleQueenSide() {
        // check if the king and rook have not moved
        Piece king = getPieceByPosition(new Position(7, 4));
        Piece rook = getPieceByPosition(new Position(7, 0));
        return king != null && rook != null && king.getPlayerColor() == PlayerColor.WHITE && rook.getPlayerColor() == PlayerColor.WHITE &&
                king.isFirstMove() && rook.isFirstMove();
    }

    public boolean blackCanCastleKingSide() {
        // check if the king and rook have not moved
        Piece king = getPieceByPosition(new Position(0, 4));
        Piece rook = getPieceByPosition(new Position(0, 7));
        return king != null && rook != null && king.getPlayerColor() == PlayerColor.BLACK && rook.getPlayerColor() == PlayerColor.BLACK &&
                king.isFirstMove() && rook.isFirstMove();
    }

    public boolean blackCanCastleQueenSide() {
        // check if the king and rook have not moved
        Piece king = getPieceByPosition(new Position(0, 4));
        Piece rook = getPieceByPosition(new Position(0, 0));
        return king != null && rook != null && king.getPlayerColor() == PlayerColor.BLACK && rook.getPlayerColor() == PlayerColor.BLACK &&
                king.isFirstMove() && rook.isFirstMove();
    }

    public String getFenString(PlayerColor activeColor) {
        StringBuilder fen = new StringBuilder();
    
        // 1. Piece placement
        for (int x = 0; x <= BOARD_SIZE; x++) {
            int emptySquares = 0;
            for (int y = 0; y <= BOARD_SIZE; y++) {
                Piece piece = getPieceByPosition(new Position(x, y));
                if (piece == null) {
                    emptySquares++;
                } else {
                    if (emptySquares > 0) {
                        fen.append(emptySquares);
                        emptySquares = 0;
                    }
                    fen.append(getFenSymbol(piece));
                }
            }
            if (emptySquares > 0) {
                fen.append(emptySquares);
            }
            if (x != BOARD_SIZE) {
                fen.append('/');
            }
        }
    
        // 2. Active color
        fen.append(' ');
        fen.append(activeColor == PlayerColor.WHITE ? 'w' : 'b');
    
        // 3. Castling rights
        fen.append(' ');
        boolean hasCastlingRights = false;
        if (whiteCanCastleKingSide()) {
            fen.append('K');
            hasCastlingRights = true;
        }
        if (whiteCanCastleQueenSide()) {
            fen.append('Q');
            hasCastlingRights = true;
        }
        if (blackCanCastleKingSide()) {
            fen.append('k');
            hasCastlingRights = true;
        }
        if (blackCanCastleQueenSide()) {
            fen.append('q');
            hasCastlingRights = true;
        }
        if (!hasCastlingRights) {
            fen.append('-');
        }
    
        // 4. En passant target square
        fen.append(' ');
        if (enPessantPosition != null) {
            fen.append(toSquareName(enPessantPosition));
        } else {
            fen.append('-');
        }
    
        // 5. Halfmove clock
        fen.append(' ');
        fen.append(halfMoveClock);
    
        // 6. Fullmove number
        fen.append(' ');
        fen.append(fullMoveNumber);
    
        return fen.toString();
    }
    
    private char getFenSymbol(Piece piece) {
        char symbol;
        switch (piece.getType()) {
            case PAWN:
                symbol = 'p';
                break;
            case ROOK:
                symbol = 'r';
                break;
            case KNIGHT:
                symbol = 'n';
                break;
            case BISHOP:
                symbol = 'b';
                break;
            case QUEEN:
                symbol = 'q';
                break;
            case KING:
                symbol = 'k';
                break;
            default:
                throw new IllegalArgumentException("Unknown piece type: " + piece.getType());
        }
        // Convert to uppercase for white pieces
        return piece.getPlayerColor() == PlayerColor.WHITE ? Character.toUpperCase(symbol) : symbol;
    }
    
    private String toSquareName(Position position) {
        char file = (char) ('a' + position.getY());
        int rank = 8 - position.getX();
        return "" + file + rank;
    }
}
