/**
 * Simplified ArchitectureRequirement type matching the backend's flat requirements model.
 */

export interface ArchitectureRequirement {
  plot_width?: number;
  plot_length?: number;
  facing_direction?: string;
  floors?: number;
  bedrooms?: number;
  bathrooms?: number;
  parking_spaces?: number;
  vastu_required?: boolean;
  style?: string;
}

export const defaultArchitectureRequirement: ArchitectureRequirement = {};
