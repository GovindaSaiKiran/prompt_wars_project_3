// purpose: Carbon Entry Schema | enforces: Quality-first
import { z } from 'zod';

export const CarbonEntrySchema = z.object({
  id: z.string().optional(),
  userId: z.string(),
  activityType: z.enum(['transport', 'energy', 'diet']),
  value: z.number(),
  unit: z.string(),
  timestamp: z.number(),
});

export type CarbonEntry = z.infer<typeof CarbonEntrySchema>;

export const CarbonCalculationSchema = z.object({
  entryId: z.string().optional(),
  co2e_kg: z.number(),
  metadata: z.record(z.string(), z.any()).optional(),
});

export type CarbonCalculation = z.infer<typeof CarbonCalculationSchema>;
