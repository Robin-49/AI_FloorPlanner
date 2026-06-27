export interface Room {
  id: string;
  name: string;
  type: 'bedroom' | 'bathroom' | 'kitchen' | 'living_room' | 'dining' | 'other';
  areaSqFt?: number;
  dimensions?: {
    width: number;
    length: number;
  };
}

export interface Floorplan {
  id: string;
  projectId: string;
  totalAreaSqFt: number;
  rooms: Room[];
  formatUrls: {
    svg?: string;
    dxf?: string;
    model3d?: string;
  };
  createdAt: Date;
}
