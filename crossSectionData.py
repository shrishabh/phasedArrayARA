#!/usr/bin/env python 

import numpy as np

def getCrossSection(energy,interactionType, particleType):
    """Returns the interaction cross section in m^2 for neutrinos/anti-neutrinos depending on whether the interaction was Charged 
        Current (CC) or Neutral Current (NC). The energy must be in GeV The formulas are taken from https://arxiv.org/pdf/hep-ph/9512364.pdf, page 18"""
    constant = 1e-36
    
    if interactionType == "CC":
        if particleType == "nu":
            sigma = 2.69*constant
            powerFactor = 0.402 # taken from the paper
            
            
        else:
            sigma = 2.53*constant
            powerFactor = 0.404
            
    elif interactionType == "NC":
        if particleType == "nu":
            sigma = 1.06*constant
            powerFactor = 0.408
        else:
            sigma = 0.98*constant
            powerFactor = 0.410
    
    print sigma, powerFactor
    energyTerm = energy**(powerFactor)
    print energyTerm
    sigma = sigma*energyTerm
    return sigma

  #index 0 is for CC, 1 is for NC
sigma_nu = {10:[.777e-37,.242e-37], 1e2:[0.697e-36,.217e-36], 1e3:[.625e-35, .199e-35], 1e4:[.454e-34, .155e-34],1e5:[.196e-33,.745e-34], 1e6:[.611e-33, .252e-33], 1e7:[.176e-32, .748e-33], 1e8:[.478e-32, .207e-32], 1e9:[.123e-31,.540e-31], 1e10:[.301e-31,.134e-31], 1e11:[.706e-31,.316e-31], 1e12:[.159e-30, .715e-31] }
sigma_nuBar = {10:[.368e-37,.130e-37], 1e2:[0.349e-36,.122e-36], 1e3:[.338e-35, .120e-35], 1e4:[.292e-34, .106e-34],1e5:[.162e-33,.631e-34], 1e6:[.582e-33, .241e-33], 1e7:[.174e-32, .742e-33], 1e8:[.477e-32, .207e-32], 1e9:[.123e-31,.540e-31], 1e10:[.301e-31,.134e-31], 1e11:[.706e-31,.316e-31], 1e12:[.159e-30, .715e-31] }

def getEffectiveVolume(triggered,thrown,generationVolume):
	"""Returns Veff and Veff_err (in Km^3) given the number of triggered events, thrown events and generation volume in Km^3"""
	Veff = (triggered*1.0/thrown)*generationVolume
	Veff_err = (np.sqrt(triggered)/thrown*1.0)*generationVolume
	return Veff, Veff_err

def getEffectiveArea(veff, veff_err=0, energy):
	""" Returns Aeff and Aeff_err (in cm^2) given the Veff and Veff_err (in Km^3) and Energy (in Units of GeV)"""
	avogadroNum = 6.022e23
	ice_density = 0.92 # g/cm^3
    ice_density *= 1e15 # converted to g/km^3 = nucleons/km^3
    crosssection = (sigma_nu[energy][0] +
                         3*sigma_nu[energy][1] +
                         sigma_nuBar[energy][0] +
                         3*sigma_nuBar[energy][1])/8
    Aeff = avogadroNum*ice_density*crosssection*veff
    Aeff_err = avogadroNum*ice_density*crosssection*veff_err
    return Aeff, Aeff_err
