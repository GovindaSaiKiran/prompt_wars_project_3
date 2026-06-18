// purpose: AI Coach Message Schema | enforces: Quality-first
import { z } from 'zod';

export const CoachMessageSchema = z.object({
  id: z.string(),
  role: z.enum(['user', 'model']),
  content: z.string(),
  timestamp: z.number(),
});

export type CoachMessage = z.infer<typeof CoachMessageSchema>;
