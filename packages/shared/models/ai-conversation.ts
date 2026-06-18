// purpose: AI Conversation Schema | enforces: Quality-first
import { z } from 'zod';
import { CoachMessageSchema } from './coach-message';

export const AiConversationSchema = z.object({
  id: z.string(),
  userId: z.string(),
  title: z.string(),
  messages: z.array(CoachMessageSchema),
  createdAt: z.number(),
  updatedAt: z.number(),
  metadata: z.record(z.string(), z.any()).optional(),
});

export type AiConversation = z.infer<typeof AiConversationSchema>;
