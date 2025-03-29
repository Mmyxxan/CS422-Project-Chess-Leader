import React from 'react';
import {
  FormControl,
  InputLabel,
  MenuItem,
  Select,
  useTheme,
} from '@material-ui/core';
import { StyledQueueContainer } from './QueueShared';
import styled from '@emotion/styled';
import { AIDifficulties, GameModes } from '../../../interfaces/Queue/GameModes';
import ButtonWithLoader from '../../../components/ButtonWithLoader/ButtonWithLoader';

const StyledFormControl = styled(FormControl)`
  width: calc(100% - ${props => props.theme.spacing(4)}px);
  margin: ${props => props.theme.spacing(2)}px;
`;

interface Props {
  joinQueue: () => void;
  joinQueueAi: (difficulty: AIDifficulties) => void;
}

const QueueJoin: React.FC<Props> = ({ joinQueue, joinQueueAi }) => {
  const [selectedMode, setSelectedMode] = React.useState(GameModes.Pvp);
  const [selectedAIMode, setSelectedAIMode] = React.useState(
    AIDifficulties.Easy,
  );
  const [isClicked, setClicked] = React.useState(false);
  const [showDifficulty, setShowDifficulty] = React.useState(false);
  const theme = useTheme();

  const handleModeChange = (event: React.ChangeEvent<{ value: unknown }>) => {
    const mode = event.target.value as GameModes;
    setSelectedMode(mode);
    setShowDifficulty(mode === GameModes.Ai);
  };

  const handleDifficultyChange = (
    event: React.ChangeEvent<{ value: unknown }>,
  ) => {
    setSelectedAIMode(event.target.value as AIDifficulties);
  };

  const handleJoinQueue = () => {
    setClicked(!isClicked);

    switch (selectedMode) {
      case GameModes.Pvp:
        joinQueue();
        return;
      case GameModes.Ai:
        // Only show difficulty selection if not already shown
        if (!showDifficulty) {
          setShowDifficulty(true);
          setClicked(false); // Reset the loading state
          return;
        }
        // If difficulty is already showing, then join the queue
        switch (selectedAIMode) {
          case AIDifficulties.Easy:
            joinQueueAi(selectedAIMode);
            break;
          case AIDifficulties.Normal:
            joinQueueAi(selectedAIMode);
            break;
          case AIDifficulties.Hard:
            joinQueueAi(selectedAIMode);
            break;
          default:
            joinQueueAi(selectedAIMode);
            return;
        }
      default:
        return;
    }
  };

  return (
    <StyledQueueContainer data-testid="queue__join">
      <StyledFormControl theme={theme}>
        <InputLabel htmlFor="select-game-mode">Mode</InputLabel>
        <Select
          id="select-game-mode"
          value={selectedMode}
          onChange={handleModeChange}
        >
          <MenuItem value={GameModes.Pvp}>PVP</MenuItem>
          <MenuItem value={GameModes.Ai}>AI</MenuItem>
        </Select>
      </StyledFormControl>

      {showDifficulty && selectedMode === GameModes.Ai && (
        <StyledFormControl theme={theme}>
          <InputLabel htmlFor="select-AI-game-mode">AI Difficulty</InputLabel>
          <Select
            id="select-AI-mode"
            value={selectedAIMode}
            onChange={handleDifficultyChange}
          >
            <MenuItem value={AIDifficulties.Easy}>Easy</MenuItem>
            <MenuItem value={AIDifficulties.Normal}>Normal</MenuItem>
            <MenuItem value={AIDifficulties.Hard}>Hard</MenuItem>
          </Select>
        </StyledFormControl>
      )}

      <ButtonWithLoader onClick={handleJoinQueue} isLoading={isClicked}>
        Find match
      </ButtonWithLoader>
    </StyledQueueContainer>
  );
};

export default QueueJoin;
