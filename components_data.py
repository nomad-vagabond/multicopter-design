import splinecloud_scipy as scsp
from dataclasses import dataclass

   
class Propeller:
    
    def __init__(self, datarow):
        self.name = datarow.iloc[0]
        self.diameter = datarow.iloc[1]
        self.width = datarow.iloc[2]
        self.blades_num = datarow.iloc[3]
        self.blade_weight = datarow.iloc[4]
        self.thrust_lim = datarow.iloc[5]
    
    def __repr__(self):
        return f"Propeller(name={self.name}, diameter={self.diameter}, width={self.width})"
    
    @property
    def weight(self):
        return self.blade_weight*self.blades_num
    

@dataclass
class Motor:
    name: str
    voltage: float
    kv: float
    weight: float
    propeller: object
    thrust_vs_throttle: object
    current_vs_throttle: object
    
    def __repr__(self):
        return f"Motor(name={self.name}, voltage={self.voltage}, kv={self.kv}, weight={self.weight}, propeller={self.propeller})"
    
    @property
    def weight_total(self):
        return self.weight + self.propeller.weight
    
    @property
    def hover_thrust(self):
        return self.thrust_vs_throttle.eval(self.hov_throttle)
    
    @property
    def hover_current(self):
        return self.current_vs_throttle.eval(self.hov_throttle)


@dataclass
class BatteryGroup:
    c_rate: float
    n_cells: int
    data: object
    weight_vs_capacity: object

    def __repr__(self):
        return f"BatteryGroup(c_rate={self.c_rate}, n_cells={self.n_cells}, data={self.data})"
    

class Battery:
    
    def __init__(self, battery_props, number):
        self.number = number
        self.data = battery_props
        self.name = battery_props.iloc[0]
        self.svalue = battery_props.iloc[1]
        self.voltage = battery_props.iloc[2]
        self.capacity = battery_props.iloc[3]
        self.length = battery_props.iloc[9]
        self.width = battery_props.iloc[10]
        self.height = battery_props.iloc[11]
        self.weight = battery_props.iloc[-1]
    
    def __repr__(self):
        return (f"Battery(name={self.name}, capacity={self.capacity}, s={self.svalue}, " +
                f"number={self.number}, total_weight={self.total_weight}, total_capacity={self.total_capacity})")
    
    @property
    def total_weight(self):
        return self.weight * self.number
    
    @property
    def total_capacity(self):
        return self.capacity * self.number

 
@dataclass
class QuadFrame:
    mass_vs_propd: object
    base_vs_propd: object
    arm_width_vs_propd: object
    payload_height_vs_propd: object
    bottom_compartment_height_vs_propd: object
    top_compartment_height_vs_propd: object
    plate_thickness_vs_propd: object
    base: None

    def __repr__(self):
        if not self.base:
            return QuadFrame.__repr__()
        
        return (f"QuadFrame(base={self.base}, weight={self.weight}, arm_width={self.arm_width} " +
                f"payload_height={self.payload_height}, bottom_compartment_height={self.bottom_compartment_height} " +
                f"top_compartment_height={self.top_compartment_height}, plate_thickness={self.plate_thickness})")
    
    def select(self, propeller_diam):
        self.base = float(self.base_vs_propd.eval(propeller_diam))
        self.weight = float(self.mass_vs_propd.eval(propeller_diam))*1e3
        self.arm_width = float(self.arm_width_vs_propd.eval(propeller_diam))
        self.payload_height = float(self.payload_height_vs_propd.eval(propeller_diam))
        self.bottom_compartment_height = float(self.bottom_compartment_height_vs_propd.eval(propeller_diam))
        self.top_compartment_height = float(self.top_compartment_height_vs_propd.eval(propeller_diam))
        self.plate_thickness = float(self.plate_thickness_vs_propd.eval(propeller_diam))
        
        return self
    
    
## Create objects
    
    
propellers_polish = {f"{datarow.iloc[1]}x{datarow.iloc[2]}": Propeller(datarow) 
                     for i, datarow in scsp.LoadSubset("sbt_M1TILb8fID1O").iterrows()}   

propellers_glossy = {f"{datarow.iloc[1]}x{datarow.iloc[2]}": Propeller(datarow) 
                     for i, datarow in scsp.LoadSubset("sbt_aNg21qxaRIQq").iterrows()}


propellers = {**propellers_polish, **propellers_glossy}


quad_frame = QuadFrame(scsp.LoadSpline("spl_Ro5GcMx8w77X"), 
                             scsp.LoadSpline("spl_Q0fYju02AOco"),
                             scsp.LoadSpline("spl_Zm1M3n8yfBA6"),
                             scsp.LoadSpline("spl_VQP8mI1oQArt"),
                             scsp.LoadSpline("spl_2IP3hOy7pq4S"),
                             scsp.LoadSpline("spl_oi5OSivXMmhn"),
                             scsp.LoadSpline("spl_j2ULEsZqp32m"),
                             None,
                            )

motors = [
    # U11II
    Motor("u11_kv120_48v_26x8.5cf", 48, 120, 772, propellers["26x8.5"],
                                    scsp.LoadSpline("spl_0PiLAYeE3Hqy"), 
                                    scsp.LoadSpline("spl_rBzrTpOCrtWk")),
    
    Motor("u11_kv120_48v_27x8.8cf", 48, 120, 772, propellers["27x8.8"],
                                    scsp.LoadSpline("spl_kQnMHUiTik9s"), 
                                    scsp.LoadSpline("spl_vmU23frwt8So")),
    
    Motor("u11_kv120_48v_28x9.2cf", 48, 120, 772, propellers["28x9.2"],
                                    scsp.LoadSpline("spl_nq4bmQ0ZKimQ"), 
                                    scsp.LoadSpline("spl_pXeEmtFMvShI")),
    
    # U7 v2.0
    Motor("u7v2_kv280_24v_18x6.1cf", 24, 280, 299, propellers["18x6.1"],
                                     scsp.LoadSpline("spl_bM1myiSsnGpZ"), 
                                     scsp.LoadSpline("spl_vuG7c9vGqlYW")),
    
    Motor("u7v2_kv280_24v_20x6cf", 24, 280, 299, propellers["20x6.0"],
                                   scsp.LoadSpline("spl_3dJ3yVPwLDvs"), 
                                   scsp.LoadSpline("spl_L1p7FAdaeTii")), 
    
    Motor("u7v2_kv280_24v_22x6.6cf", 24, 280, 299, propellers["22x6.6"],
                                     scsp.LoadSpline("spl_nx7fP4anNGna"), 
                                     scsp.LoadSpline("spl_6KccNb4n7YRY")), 
    
    Motor("u7v2_kv420_22.2v_15x5cf", 22.2, 420, 299, propellers["15x5.0"],
                                     scsp.LoadSpline("spl_iBV4jySr6NVb"), 
                                     scsp.LoadSpline("spl_AcMRNaIKdcj2")),
    
    Motor("u7v2_kv420_22.2v_16x5.4cf", 22.2, 420, 299, propellers["16x5.4"],
                                       scsp.LoadSpline("spl_osGNPoew2zPz"), 
                                       scsp.LoadSpline("spl_76trp37EhB2l")),
    
    Motor("u7v2_kv420_25v_17x5.8cf", 25, 420, 299, propellers["17x5.8"],
                                     scsp.LoadSpline("spl_KE23Ml3PCmVo"), 
                                     scsp.LoadSpline("spl_VO5gFup8V9E0")),
    
    Motor("u7v2_kv420_25v_18x6.1cf", 25, 420, 299, propellers["18x6.1"],
                                     scsp.LoadSpline("spl_S9h3Y31e1aYd"), 
                                     scsp.LoadSpline("spl_kSUQd4WMIj0d")),
    
    Motor("u7v2_kv490_14.8v_17x5.8cf", 14.8, 490, 299, propellers["17x5.8"],
                                       scsp.LoadSpline("spl_CgnIEbSMBUXW"), 
                                       scsp.LoadSpline("spl_sdcM1TMFDBZu")),
    
    Motor("u7v2_kv490_14.8v_18x6.1cf", 14.8, 490, 299, propellers["18x6.1"],
                                       scsp.LoadSpline("spl_p54g84itsn1S"), 
                                       scsp.LoadSpline("spl_fkFwik4dJJka")),
    
    Motor("u7v2_kv490_22.2v_15x5cf", 22.2, 490, 299, propellers["15x5.0"],
                                     scsp.LoadSpline("spl_hgw9Q2ntda41"), 
                                     scsp.LoadSpline("spl_qmsiPjO0DE36")),
    
    Motor("u7v2_kv490_22.2v_16x5.4cf", 22.2, 490, 299, propellers["16x5.4"],
                                       scsp.LoadSpline("spl_0Z6wIOzYm2HB"), 
                                       scsp.LoadSpline("spl_A5oL7ETiSSKU")),
    
    Motor("u7v2_kv490_25v_17x5.8cf", 25, 490, 299, propellers["17x5.8"],
                                     scsp.LoadSpline("spl_sKwnDiVJCSej"), 
                                     scsp.LoadSpline("spl_KlMac8fsS7D0")),
    
    Motor("u7v2_kv490_25v_18x6.1cf", 25, 490, 299, propellers["18x6.1"],
                                     scsp.LoadSpline("spl_mq9tR6ud0SxJ"), 
                                     scsp.LoadSpline("spl_Qys5gAYUVrYU")),
    
    # U5
    Motor("u5_kv400_v22.2_14x4.8cf", 22.2, 400, 195, propellers["14x4.8"],
                                     scsp.LoadSpline("spl_X7Jvv7xHFmhu"), 
                                     scsp.LoadSpline("spl_BVuVxfcZAeIV")),

    Motor("u5_kv400_v22.2_15x5cf", 22.2, 400, 195, propellers["15x5.0"],
                                   scsp.LoadSpline("spl_Ze8sk9Tp0BGx"), 
                                   scsp.LoadSpline("spl_nJim7zfAEz6j")),
    
    Motor("u5_kv400_v22.2_16x5.4cf", 22.2, 400, 195, propellers["16x5.4"],
                                     scsp.LoadSpline("spl_TNvnoyH1apaJ"), 
                                     scsp.LoadSpline("spl_M8OQHdM8Vxed")),
    
    # U3
    Motor("u3_kv700_11.1v_12x4cf", 11.1, 700, 128, propellers["12x4.0"],
                                   scsp.LoadSpline("spl_WsuqU1GAhsfY"), 
                                   scsp.LoadSpline("spl_GOfFHyLjvcJc")),
    
    Motor("u3_kv700_11.1v_13x4.4cf", 11.1, 700, 128, propellers["13x4.4"],
                                     scsp.LoadSpline("spl_HQYSBVrq78qX"), 
                                     scsp.LoadSpline("spl_X8daanZbEwhg")),
    
    Motor("u3_kv700_11.1v_14x4.8cf", 11.1, 700, 128, propellers["14x4.8"],
                                     scsp.LoadSpline("spl_wkI9aMppMP53"), 
                                     scsp.LoadSpline("spl_ZrE3riufdxwP")),
    
    Motor("u3_kv700_14.8v_12x4cf", 14.8, 700, 128, propellers["12x4.0"],
                                   scsp.LoadSpline("spl_0nWa8OguX76J"), 
                                   scsp.LoadSpline("spl_ddabfX7PR6ad")),
    
    Motor("u3_kv700_14.8v_13x4.4cf", 14.8, 700, 128, propellers["13x4.4"],
                                     scsp.LoadSpline("spl_LxyHKihZmVpu"), 
                                     scsp.LoadSpline("spl_LZeRi2ERFuEr")),

]

battery_groups = {
    "hp-g8-c45": {
        "2S": BatteryGroup(45, 2, scsp.LoadSubset("sbt_H7aWow0A5Xt1"), scsp.LoadSpline("spl_aZZe5tZwWzcG")),
        "3S": BatteryGroup(45, 3, scsp.LoadSubset("sbt_MU5QnB2sOar8"), scsp.LoadSpline("spl_SHuGqVd7XUxj")),
        "4S": BatteryGroup(45, 4, scsp.LoadSubset("sbt_1bOEqPQMDtMl"), scsp.LoadSpline("spl_24IJKiB91ruZ")),
        "6S": BatteryGroup(45, 6, scsp.LoadSubset("sbt_02R8n6kkWm74"), scsp.LoadSpline("spl_Kw6Cf0AqNP0q")),
    },
    
    "hp-g8-c30": {
        "2S": BatteryGroup(30, 2, scsp.LoadSubset("sbt_TFpLUUxHremY"), scsp.LoadSpline("spl_GdsPkRgWiCW9")),
        "3S": BatteryGroup(30, 3, scsp.LoadSubset("sbt_q2nfXP4zhw3y"), scsp.LoadSpline("spl_bzZQptrgnGfG")),
        "4S": BatteryGroup(30, 4, scsp.LoadSubset("sbt_wOfrBbRTlCMD"), scsp.LoadSpline("spl_lurbWvSkx2HP")),
        "6S": BatteryGroup(30, 6, scsp.LoadSubset("sbt_7qzkLibxUQwf"), scsp.LoadSpline("spl_2kSEDWKCBS65")),
    }

}