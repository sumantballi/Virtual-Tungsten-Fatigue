
import numpy as np

def scf_for_pore(sqrt_area, aspect_ratio, is_surface):
    base = 1.0 + 2.0*(sqrt_area/20e-6)
    shape = 1.0 + (1.0 - np.clip(aspect_ratio, 0.1, 1.0))*1.5
    surf = np.where(is_surface==1, 1.35, 1.0)
    return base*shape*surf

def kitagawa_allowable_stress(sqrt_area, sigma_u, deltaK_th):
    a = (sqrt_area/np.sqrt(np.pi))**2
    small_defect_limit = deltaK_th / np.sqrt(np.pi*a + 1e-20)
    large_defect_limit = 0.5*sigma_u
    return (small_defect_limit*large_defect_limit)/(small_defect_limit + large_defect_limit + 1e-20)*2.0

def paris_life(a0, a_crit, delta_sigma_eff, E, deltaK_th, C, m):
    Y = 1.0
    if Y*delta_sigma_eff*np.sqrt(np.pi*a0) < deltaK_th:
        return 1e12
    alpha = C*(Y*delta_sigma_eff*np.sqrt(np.pi))**m
    p = m/2.0
    if abs(m-2.0) > 1e-9:
        N = ( (a_crit**(1.0-p) - a0**(1.0-p)) / ( (1.0-p) * alpha ) )
    else:
        N = ( np.log(a_crit/a0) / alpha )
    return max(N, 0.0)
