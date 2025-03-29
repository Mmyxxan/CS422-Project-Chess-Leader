import axios from 'axios';
import { AIDifficulties } from '../../interfaces/Queue/GameModes';

export const fetchJoinQueueAi = (login: string, difficulty: AIDifficulties) =>
  axios.post(`${process.env.BASE_API_URL}/queue/with-ai`, {
    login,
    difficulty,
  });
