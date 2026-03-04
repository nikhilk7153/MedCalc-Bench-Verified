import unit_converter_new
from rounding import round_number

def compute_ldl(total_cholesterol, hdl_cholesterol, triglycerides):
    total_cholestrol = unit_converter_new.conversion(total_cholesterol[0], 'total cholesterol', 386.654, None, total_cholesterol[1], 'mg/dL')
    hdl_cholestrol = unit_converter_new.conversion(hdl_cholesterol[0], 'hdl cholesterol', 386.654, None, hdl_cholesterol[1], 'mg/dL')
    triglycerides = unit_converter_new.conversion(triglycerides[0], 'triglycerides', 861.338, None, triglycerides[1], 'mg/dL')
    answer = total_cholestrol - hdl_cholestrol - triglycerides / 5
    return answer
