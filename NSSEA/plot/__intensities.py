
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

import numpy  as np
import pandas as pd
import xarray as xr

import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.backends.backend_pdf as mpdf

from ..__tools import ProgressBar


###############
## Functions ##
###############

def intensities( clim , ofile , event = None , ci = 0.05 , verbose = False ): ##{{{
	"""
	NSSEA.plot.intensities
	======================
	
	Plot intensities (IF,IC,dI) along time
	
	Arguments
	---------
	clim      : NSSEA.Climatology
		Climatology with stats computed
	ofile     : str
		output file
	event     : NSSEA.Event
		If event is None, clim.event is used
	ci        : float
		Size of confidence interval, default is 0.05 (95% confidence)
	verbose   : bool
		Print (or not) state of execution
	"""
	
	pb = ProgressBar( clim.n_model + 1 , "plot.intensities" , verbose = verbose )
#	["pC","pF","IC","IF","PR","dI"]
	
	if event is None:
		event = clim.event
	
	## Find quantile and best estimate
	qstats = clim.statistics[:,1:,:,:].loc[:,:,["IC","IF","dI"],:].quantile( [ ci / 2. , 0.5 , 1 - ci / 2] , dim = "sample" ).assign_coords( quantile = ["ql","BE","qu"] )
	if not clim.BE_is_median:
		qstats.loc["BE",:,:,:] = clim.statistics.loc[:,"BE",["IC","IF","dI"],:]
	pb.print()
	
	pdf = mpdf.PdfPages( ofile )
	
	yminI  = float(qstats.loc[:,:,["IF","IC"],:].min())
	ymaxI  = float(qstats.loc[:,:,["IF","IC"],:].max())
	ymindI = float(qstats.loc[:,:,"dI",:].min())
	ymaxdI = float(qstats.loc[:,:,"dI",:].max())
	
	ylabel = "\mathrm{(" + event.unit + ")}"
	
	for m in clim.model:
		nrow,ncol = 3,1
		fs = 10
		fig = plt.figure( figsize = ( fs * ncol , 0.4 * fs * nrow ) )
		
		ax = fig.add_subplot( nrow , ncol , 1 )
		ax.plot( qstats.time , qstats.loc["BE",:,"IF",m] , color = "red" , linestyle = "-" , marker = "" )
		ax.fill_between( qstats.time , qstats.loc["ql",:,"IF",m] , qstats.loc["qu",:,"IF",m] , color = "red" , alpha = 0.5 )
		ax.set_title( " ".join(m.split("_")) )
		ax.set_ylim( (yminI,ymaxI) )
		ax.set_xticks([])
		ax.set_ylabel( r"${}$".format( "\mathbf{I}^F_t\ " + ylabel ) )
		xlim = ax.get_xlim()
		ylim = ax.get_ylim()
		ax.vlines( event.time , ylim[0] , ylim[1] , linestyle = "--" , color = "black" )
		ax.hlines( qstats.loc["BE",event.time,"IF",m] , xlim[0] , xlim[1] , color = "black" , linestyle = "--" )
		ax.set_xlim(xlim)
		ax.set_ylim(ylim)
		
		ax = fig.add_subplot( nrow , ncol , 2 )
		ax.plot( qstats.time , qstats.loc["BE",:,"IC",m] , color = "blue" , linestyle = "-" , marker = "" )
		ax.fill_between( qstats.time , qstats.loc["ql",:,"IC",m] , qstats.loc["qu",:,"IC",m] , color = "blue" , alpha = 0.5 )
		ax.set_ylim( (yminI,ymaxI) )
		ax.set_xticks([])
		ax.set_ylabel( r"${}$".format( "\mathbf{I}^C_t\ " + ylabel ) )
		xlim = ax.get_xlim()
		ylim = ax.get_ylim()
		ax.vlines( event.time , ylim[0] , ylim[1] , linestyle = "--" , color = "black" )
		ax.hlines( qstats.loc["BE",event.time,"IC",m] , xlim[0] , xlim[-1] , color = "black" , linestyle = "--" )
		ax.set_xlim(xlim)
		ax.set_ylim(ylim)
		
		ax = fig.add_subplot( nrow , ncol , 3 )
		ax.plot( qstats.time , qstats.loc["BE",:,"dI",m] , color = "red" , linestyle = "-" , marker = "" )
		ax.fill_between( qstats.time , qstats.loc["ql",:,"dI",m] , qstats.loc["qu",:,"dI",m] , color = "red" , alpha = 0.5 )
		ax.set_ylim( (ymindI,ymaxdI) )
		ax.set_xlabel( "Time" )
		ax.set_ylabel( r"${}$".format( "\Delta\mathbf{I}_t\ " + ylabel ) )
		xlim = ax.get_xlim()
		ylim = ax.get_ylim()
		ax.vlines( event.time , ylim[0] , ylim[1] , linestyle = "--" , color = "black" )
		ax.hlines( qstats.loc["BE",event.time,"dI",m] , xlim[0] , xlim[-1] , color = "black" , linestyle = "--" )
		ax.hlines( 0 , xlim[0] , xlim[-1] , color = "black" , linestyle = "-" )
		ax.set_xlim(xlim)
		ax.set_ylim(ylim)
		
		
		fig.set_tight_layout(True)
		pdf.savefig( fig )
		plt.close(fig)
		pb.print()
	
	pdf.close()
	
	pb.end()
	
##}}}


