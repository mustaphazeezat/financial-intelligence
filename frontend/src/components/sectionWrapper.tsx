import type { ReactNode } from 'react';

type SectionWrapperProps = {
  children: ReactNode;
  className?: string;
};

function SectionWrapper({ children, className }: SectionWrapperProps) {
  return (
    <div className={`mx-auto max-w-7xl ${className}`}>{children}</div>
  )
}

export default SectionWrapper