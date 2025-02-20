# -*- coding: utf-8 -*-

##################################################################################
##################################################################################
##                                                                              ##
## Copyright Yoann Robin, 2020                                                  ##
##                                                                              ##
## yoann.robin.k@gmail.com                                                      ##
##                                                                              ##
## This software is a computer program that is part of the NSSEA                ##
## (Non-Stationary Statistics for Extreme Attribution) This library makes it    ##
## possible to infer the probability of an (extreme) event in the factual /     ##
## counter-factual world (without anthropic forcing) to attribute it to climate ##
## change.                                                                      ##
##                                                                              ##
## This software is governed by the CeCILL-C license under French law and       ##
## abiding by the rules of distribution of free software.  You can  use,        ##
## modify and/ or redistribute the software under the terms of the CeCILL-C     ##
## license as circulated by CEA, CNRS and INRIA at the following URL            ##
## "http://www.cecill.info".                                                    ##
##                                                                              ##
## As a counterpart to the access to the source code and  rights to copy,       ##
## modify and redistribute granted by the license, users are provided only      ##
## with a limited warranty  and the software's author,  the holder of the       ##
## economic rights,  and the successive licensors  have only  limited           ##
## liability.                                                                   ##
##                                                                              ##
## In this respect, the user's attention is drawn to the risks associated       ##
## with loading,  using,  modifying and/or developing or reproducing the        ##
## software by the user in light of its specific status of free software,       ##
## that may mean  that it is complicated to manipulate,  and  that  also        ##
## therefore means  that it is reserved for developers  and  experienced        ##
## professionals having in-depth computer knowledge. Users are therefore        ##
## encouraged to load and test the software's suitability as regards their      ##
## requirements in conditions enabling the security of their systems and/or     ##
## data to be ensured and,  more generally, to use and operate it in the        ##
## same conditions as regards security.                                         ##
##                                                                              ##
## The fact that you are presently reading this means that you have had         ##
## knowledge of the CeCILL-C license and that you accept its terms.             ##
##                                                                              ##
##################################################################################
##################################################################################

##################################################################################
##################################################################################
##                                                                              ##
## Copyright Yoann Robin, 2020                                                  ##
##                                                                              ##
## yoann.robin.k@gmail.com                                                      ##
##                                                                              ##
## Ce logiciel est un programme informatique faisant partie de la librairie     ##
## NSSEA (Non-Stationary Statistics for Extreme Attribution). Cette librairie   ##
## permet d'estimer la probabilité d'un evenement (extreme) dans le monde       ##
## factuel / contre factuel (sans forcage anthropogenique) et de l'attribuer au ##
## changement climatique.                                                       ##
##                                                                              ##
## Ce logiciel est régi par la licence CeCILL-C soumise au droit français et    ##
## respectant les principes de diffusion des logiciels libres. Vous pouvez      ##
## utiliser, modifier et/ou redistribuer ce programme sous les conditions       ##
## de la licence CeCILL-C telle que diffusée par le CEA, le CNRS et l'INRIA     ##
## sur le site "http://www.cecill.info".                                        ##
##                                                                              ##
## En contrepartie de l'accessibilité au code source et des droits de copie,    ##
## de modification et de redistribution accordés par cette licence, il n'est    ##
## offert aux utilisateurs qu'une garantie limitée.  Pour les mêmes raisons,    ##
## seule une responsabilité restreinte pèse sur l'auteur du programme, le       ##
## titulaire des droits patrimoniaux et les concédants successifs.              ##
##                                                                              ##
## A cet égard  l'attention de l'utilisateur est attirée sur les risques        ##
## associés au chargement,  à l'utilisation,  à la modification et/ou au        ##
## développement et à la reproduction du logiciel par l'utilisateur étant       ##
## donné sa spécificité de logiciel libre, qui peut le rendre complexe à        ##
## manipuler et qui le réserve donc à des développeurs et des professionnels    ##
## avertis possédant  des  connaissances  informatiques approfondies.  Les      ##
## utilisateurs sont donc invités à charger  et  tester  l'adéquation  du       ##
## logiciel à leurs besoins dans des conditions permettant d'assurer la         ##
## sécurité de leurs systèmes et ou de leurs données et, plus généralement,     ##
## à l'utiliser et l'exploiter dans les mêmes conditions de sécurité.           ##
##                                                                              ##
## Le fait que vous puissiez accéder à cet en-tête signifie que vous avez       ##
## pris connaissance de la licence CeCILL-C, et que vous en avez accepté les    ##
## termes.                                                                      ##
##                                                                              ##
##################################################################################
##################################################################################

###############
## Libraries ##
###############

import numpy             as np
import scipy.stats       as sc
import scipy.interpolate as sci
import scipy.special     as scs
import SDFC              as sd
import SDFC.link         as sdl

from .__AbstractModel import AbstractModel


#############
## Classes ##
#############

class GEVMin(AbstractModel):
	
	def __init__( self , loc_cst = False , scale_cst = False , shape_cst = True , **kwargs ):##{{{
		l_scale = kwargs.get("l_scale")
		if l_scale is None: l_scale = sdl.ULExponential()
		lparams = []
		lparams.append( { "name" : "loc"   , "is_cst" :   loc_cst , "link" : kwargs.get("l_loc")   , "name_tex" : r"\mu"    } )
		lparams.append( { "name" : "scale" , "is_cst" : scale_cst , "link" : l_scale               , "name_tex" : r"\sigma" } )
		lparams.append( { "name" : "shape" , "is_cst" : shape_cst , "link" : kwargs.get("l_shape") , "name_tex" : r"\xi"    } )
		AbstractModel.__init__( self , "GEV" , sc.genextreme , sd.GEV , lparams , **kwargs )
	##}}}
	
	
	## Fit methods
	##============
	
	def _get_sdkwargs( self , X ):##{{{
		sdkwargs = {}
		for p in self.lparams:
			sdkwargs[ "l_" + p ] = self.lparams[p].link
			if not self.lparams[p].is_cst:
				sdkwargs[ "c_" + p ] = -X
		return sdkwargs
	##}}}
	
	## Accessors
	##==========
	
	def set_covariable( self , X , t ):##{{{
		AbstractModel.set_covariable( self , -X , t )
	##}}}
	
	def fit( self , Y , X ):##{{{
		AbstractModel.fit( self , -Y , X )
	##}}}
	
	def drawn_bayesian( self , Y , X  , n_mcmc_drawn , prior , min_rate_accept = 0.25 , **kwargs ):##{{{
		return AbstractModel.drawn_bayesian( self , -Y , X , n_mcmc_drawn , prior , min_rate_accept , **kwargs )
	##}}}
	
	## Stats methods
	##==============
	
	def loct( self , t ):##{{{
		return -self.lparams["loc"](t)
	##}}}
	
	def scalet( self , t ):##{{{
		return self.lparams["scale"](t)
	##}}}
	
	def shapet( self , t ):##{{{
		return self.lparams["shape"](t)
	##}}}
	
	def meant( self , t ):##{{{
		shapet = self.shapet(t)
		idx = np.abs(shapet) > 1e-8
		cst = np.zeros(shapet) + np.euler_gamma
		cst[idx] = ( scs.gamma( 1 - shapet[idx] ) - 1 ) / shapet[idx]
		return - (self._loct(t) + self._scalet(t) * cst)
	##}}}
	
	def mediant( self , t ):##{{{
		return - (self.loct(t) + self.scalet(t) * ( np.pow( np.log(2) , - self.shapet(t) ) - 1. ) / self.shapet(t))
	##}}}
	
	def upper_boundt( self , t ):##{{{
		"""
		Upper bound of GEV model (can be infinite)
		
		Parameters
		----------
		t : np.array
			Time
		
		Results
		-------
		bound : np.array
			bound at time t
		"""
		loc   = -self.loct(t)
		scale =  self.scalet(t)
		shape =  self.shapet(t)
		bound = loc - scale / shape
		idx   = np.logical_not( shape < 0 )
		bound[idx] = np.inf
		return -bound
	##}}}
	
	def lower_boundt( self , t ):##{{{
		"""
		Lower bound of GEV model (can be -infinite)
		
		Parameters
		----------
		t : np.array
			Time
		
		Results
		-------
		bound : np.array
			bound at time t
		"""
		loc   = -self.loct(t)
		scale =  self.scalet(t)
		shape =  self.shapet(t)
		bound = loc - scale / shape
		idx   = shape < 0
		bound[idx] = - np.inf
		return -bound
	##}}}
	
	
	def _get_sckwargs( self , t ):##{{{
		sckwargs = AbstractModel._get_sckwargs( self , t )
		sckwargs["c"] = - sckwargs["shape"]
		del sckwargs["shape"]
		return sckwargs
	##}}}
	
	def rvs( self , t ):##{{{
		"""
		Random value generator
		
		Parameters
		----------
		t : np.array
			Time
		
		Returns
		-------
		Y : np.array
			A time series following the NS law
		"""
		sckwargs = self._get_sckwargs(t)
		return - self.law.rvs( size = t.size , **sckwargs )
	##}}}
	
	def cdf( self , Y , t ):##{{{
		"""
		Cumulative Distribution Function (inverse of quantile function)
		
		Parameters
		----------
		Y : np.array
			Value to estimate the CDF
		t : np.array
			Time
		
		Returns
		-------
		q : np.array
			CDF value
		"""
		sckwargs = self._get_sckwargs(t)
		return self.law.sf( -Y , **sckwargs )
	##}}}
	
	def icdf( self , q , t ):##{{{
		"""
		inverse of Cumulative Distribution Function 
		
		Parameters
		----------
		q : np.array
			Values to estimate the quantile
		t : np.array
			Time
		
		Returns
		-------
		Y : np.array
			Quantile
		"""
		sckwargs = self._get_sckwargs(t)
		return -self.law.isf( q , **sckwargs )
	##}}}
	
	def sf( self , Y , t ):##{{{
		"""
		Survival Function (1-CDF)
		
		Parameters
		----------
		Y : np.array
			Value to estimate the survival function
		t : np.array
			Time
		
		Returns
		-------
		q : np.array
			survival value
		"""
		sckwargs = self._get_sckwargs(t)
		return self.law.cdf( -Y , **sckwargs )
	##}}}
	
	def isf( self , q , t ):##{{{
		"""
		inverse of Survival Function
		
		Parameters
		----------
		q : np.array
			Values to estimate the quantile
		t : np.array
			Time
		
		Returns
		-------
		Y : np.array
			values
		"""
		sckwargs = self._get_sckwargs(t)
		return -self.law.ppf( q , **sckwargs )
	##}}}
	
	def kstest( self , Y ): ##{{{
		
		loc   = self.loct(Y.index).squeeze()
		scale = self.scalet(Y.index).squeeze()
		shape = self.shapet(Y.index).squeeze()
		Z     = - ( Y.values.squeeze() - loc ) / scale
		return list(sc.kstest( Z , lambda x : sc.genextreme.cdf( x , loc = 0 , scale = 1 , c = - shape ) ) )
	##}}}
	
