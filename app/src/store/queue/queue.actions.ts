import {
  JoinQueueAction,
  JoinQueueAiAction,
  LeaveQueueAction,
  QueueActionTypes,
  QueueErrorAction,
  QueueGameFoundAction,
  QueueJoinedAction,
  QueueLeftAction,
} from './queue.types';

import { AIDifficulties, GameModes } from '../../interfaces/Queue/GameModes';

export const joinQueue = (): JoinQueueAction => ({
  type: QueueActionTypes.JOIN_QUEUE,
});

export const queueJoined = (timeJoined: string): QueueJoinedAction => ({
  type: QueueActionTypes.QUEUE_JOINED,
  payload: {
    timeJoined,
  },
});

export const queueGameFound = (gameId: string): QueueGameFoundAction => ({
  type: QueueActionTypes.QUEUE_GAME_FOUND,
  payload: {
    gameId,
  },
});

export const queueLeft = (login: string): QueueLeftAction => ({
  type: QueueActionTypes.QUEUE_LEFT,
  payload: {
    login,
  },
});

export const leaveQueue = (): LeaveQueueAction => ({
  type: QueueActionTypes.LEAVE_QUEUE,
});

export const joinQueueAi = (difficulty: AIDifficulties): JoinQueueAiAction => ({
  type: QueueActionTypes.JOIN_QUEUE_AI,
  payload: {
    difficulty,
  },
});

export const queueError = (error: string): QueueErrorAction => ({
  type: QueueActionTypes.QUEUE_ERROR,
  payload: {
    error,
  },
});
