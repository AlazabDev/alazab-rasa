import { z } from "zod"

export const codeSchema = z.object({
  action: z.enum(["fix","explain","optimize","secure"]),
  language: z.string(),
  code: z.string().min(1).max(10000),
})
