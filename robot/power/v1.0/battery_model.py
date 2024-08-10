from dataclasses import dataclass
from typing import List

@dataclass
class BatteryCellConfig:
    critical_voltage: float
    empty_voltage: float
    nominal_voltage: float
    full_voltage: float

class LiPoBattery:
    def __init__(self, num_cells: int, cell_config: BatteryCellConfig, capacity_mah: float, c_rating: float):
        self.num_cells = num_cells
        self.cell_config = cell_config

        self.capacity = capacity_mah / 1000.0
        self.c_rating = c_rating

    def get_num_cells(self):
        return self.num_cells

    def get_cell_critical_voltage(self, cell: int):
        if cell < 1 or cell > self.num_cells:
            raise Exception(f"invalid cell number: {cell}")

        return cell * self.cell_config.critical_voltage
    
    def get_cell_empty_voltage(self, cell: int):
        if cell < 1 or cell > self.num_cells:
            raise Exception(f"invalid cell number: {cell}")
        
        return cell * self.cell_config.empty_voltage

    def get_cell_nominal_voltage(self, cell: int):
        if cell < 1 or cell > self.num_cells:
            raise Exception(f"invalid cell number: {cell}")
        
        return cell * self.cell_config.nominal_voltage
    
    def get_cell_full_voltage(self, cell: int):
        if cell < 1 or cell > self.num_cells:
            raise Exception(f"invalid cell number: {cell}")
        
        return cell * self.cell_config.full_voltage

    def get_pack_critical_voltage(self):
        return self.num_cells * self.cell_config.critical_voltage
    
    def get_pack_empty_voltage(self):
        return self.num_cells * self.cell_config.empty_voltage
    
    def get_pack_nominal_voltage(self):
        return self.num_cells * self.cell_config.nominal_voltage
    
    def get_pack_max_voltage(self):
        return self.num_cells * self.cell_config.full_voltage
    
    def battery_duration_at_current(self, current):
        return self.capacity / current

