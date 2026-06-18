// purpose: User Sustainability Profile | enforces: Quality-first
import { z } from 'zod';

export const UserSustainabilityProfileSchema = z.object({
  id: z.string(),
  userId: z.string(),
  travelData: z.record(z.string(), z.any()).optional(),
  electricityUsage: z.record(z.string(), z.any()).optional(),
  foodHabits: z.record(z.string(), z.any()).optional(),
  waterConsumption: z.record(z.string(), z.any()).optional(),
  shoppingHabits: z.record(z.string(), z.any()).optional(),
});

export type UserSustainabilityProfile = z.infer<typeof UserSustainabilityProfileSchema>;
