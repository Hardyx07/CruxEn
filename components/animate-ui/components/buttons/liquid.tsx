'use client';

import * as React from 'react';
import { cva, type VariantProps } from 'class-variance-authority';

import {
  LiquidButton as LiquidButtonPrimitive,
  type LiquidButtonProps as LiquidButtonPrimitiveProps,
} from '@/components/animate-ui/primitives/buttons/liquid';
import { cn } from '@/lib/utils';

const buttonVariants = cva(
  "inline-flex items-center justify-center gap-2 whitespace-nowrap rounded-xl text-base font-bold transition-[box-shadow,_color,_background-color,_border-color,_outline-color,_text-decoration-color,_fill,_stroke] disabled:pointer-events-none disabled:opacity-50 [&_svg]:pointer-events-none [&_svg:not([class*='size-'])]:size-5 shrink-0 [&_svg]:shrink-0 outline-none focus-visible:border-ring focus-visible:ring-ring/50 focus-visible:ring-[3px] aria-invalid:ring-destructive/20 dark:aria-invalid:ring-destructive/40 aria-invalid:border-destructive",
  {
    variants: {
      variant: {
        default:
          '[--liquid-button-background-color:oklch(0.98_0_0)] [--liquid-button-color:oklch(0.05_0_0)] text-background hover:text-background shadow-2xl',
        destructive:
          '[--liquid-button-background-color:oklch(0.55_0.22_25)] [--liquid-button-color:oklch(0.98_0_0)] text-white shadow-2xl focus-visible:ring-destructive/20 dark:focus-visible:ring-destructive/40',
        secondary:
          '[--liquid-button-background-color:oklch(0.25_0_0)] [--liquid-button-color:oklch(0.98_0_0)] text-foreground hover:text-foreground shadow-2xl',
        ghost:
          '[--liquid-button-background-color:transparent] [--liquid-button-color:oklch(0.98_0_0)] text-foreground hover:text-foreground shadow-xl',
      },
      size: {
        default: 'h-12 px-6 py-3 has-[>svg]:px-5',
        sm: 'h-10 rounded-lg gap-1.5 px-4 has-[>svg]:px-3',
        lg: 'h-14 rounded-xl px-8 py-4 has-[>svg]:px-6 text-lg',
        icon: 'size-12',
        'icon-sm': 'size-10 rounded-lg',
        'icon-lg': 'size-14 rounded-xl',
      },
    },
    defaultVariants: {
      variant: 'default',
      size: 'lg',
    },
  },
);

type LiquidButtonProps = LiquidButtonPrimitiveProps &
  VariantProps<typeof buttonVariants>;

function LiquidButton({
  className,
  variant,
  size,
  ...props
}: LiquidButtonProps) {
  return (
    <LiquidButtonPrimitive
      className={cn(buttonVariants({ variant, size, className }))}
      {...props}
    />
  );
}

export { LiquidButton, buttonVariants, type LiquidButtonProps };
