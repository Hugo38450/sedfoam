import numpy as np
import fluidfoam
from pylab import figure, subplot, grid, axis, xlabel, ylabel, show
from pylab import xticks, savefig
from pylab import matplotlib
import matplotlib.gridspec as gridspec
from matplotlib import rc
import matplotlib as mpl


def readOpenFoam(sol):
    import subprocess
    #
    # Reading SedFoam results
    #
    #
    tread = 'latestTime'
    Nt = 1
    X, Y, Z = fluidfoam.readmesh(sol)
    alpha = fluidfoam.readscalar(sol, tread, 'alpha_a')
    Ua = fluidfoam.readvector(sol, tread, 'Ua')
    Ub = fluidfoam.readvector(sol, tread, 'Ub')
    Tauf = fluidfoam.readtensor(sol, tread, 'Taub')
    Taus = fluidfoam.readtensor(sol, tread, 'Taua')

    return Nt, Y, Ua[0, :], Ub[0, :], alpha, Tauf[3, :], Taus[3, :]

#
# Change fontsize
#
rc('text', usetex=True)
#
# linewidth
#
lw = 3
ms = 8
matplotlib.rcParams.update({'font.size': 20})
mpl.rcParams['lines.linewidth'] = lw
mpl.rcParams['lines.markersize'] = ms

#
gs = gridspec.GridSpec(1, 3)
gs.update(left=0.065, right=0.975, top=0.95,
          bottom=0.15, wspace=0.1, hspace=0.15)
#
# Figure size
#
figwidth = 13.5
figheight = 5

#
# Parameters
#
rho_f = 1000.
rho_s = 1190.
rs = 1.5e-3
alphasmax = 0.65

Ustarexp = 0.05
#
# load experimental results
#
[Zexpp, Phiexp] = np.loadtxt(
    'DATA/Revil-Baudard2015_phi.txt', skiprows=1, unpack=True)
[Zexp, Uexp, uwexp] = np.loadtxt(
    'DATA/Revil-Baudard2015_uRxz.txt', skiprows=1, unpack=True)

#########################################
#
# Loading OpenFoam results
#
basepath = '../'

Nx = 1
Ny = 400
Nz = 1

casedir = '1DSheetFlow/'
label = '$\mu(I)$+ML'

############################################
# case 1
#
solpath = basepath + casedir
Nt, y, ua, ub, alpha0, Tauxy, Tausxy = readOpenFoam(solpath)

#
# Plots
#

zmin = -2
zmax = 25

Z0num = -0.01 - rs

umax = 1.
#
#
# figure 1
#
#
fig = figure(num=1, figsize=(figwidth, figheight),
             dpi=60, facecolor='w', edgecolor='w')

x_ticks = np.array([0,  2.5, 5])
x_labels = ['0', '2.5', '5']
#
# ax1
#
ax1 = subplot(gs[0, 0])
p1_5 = ax1.plot(ub, (y + Z0num) / (2. * rs), '-b')
p1_4 = ax1.plot(ua, (y + Z0num) / (2. * rs), '-r')
p1_1 = ax1.plot(Uexp[:], Zexp[:] / (2. * rs), 'ok', markersize=ms)
ylabel(r'$y/d_p$')
xlabel(r'$U (m/s)$')
axis([0, umax, zmin, zmax])
grid()
#
# ax2
#
ax2 = subplot(gs[0, 1])
p2_3 = ax2.plot(alpha0, (y + Z0num) / (2. * rs), '-r', label=label)
p2_1 = ax2.plot(Phiexp, Zexpp / (2. * rs), 'ok',
                markersize=ms, label='experiment')
handles2, labels2 = ax2.get_legend_handles_labels()
ax2.legend(handles2[0:4], labels2[0:4], loc=1, prop={'size': 14})
ax2.set_yticklabels([])
xlabel(r'$\alpha$')
axis([0, alphasmax, zmin, zmax])
grid()

#
# ax3
#
ax3 = subplot(gs[0, 2])
p3_2 = ax3.plot( Tauxy, (y + Z0num) / (2. * rs), '-b')
p3_2 = ax3.plot(Tausxy, (y + Z0num) / (2. * rs), '--r')
p3_1 = ax3.plot(rho_f * uwexp, Zexp / (2. * rs), 'ok',
                markersize=ms, label='experiment')
ax3.set_yticklabels([])
xlabel(r'$\tau_{xz} (Pa)$')
axis([0, 3, zmin, zmax])
xticks(x_ticks, x_labels)
grid()


savefig('Figures/res1_tuto3.png', facecolor='w', edgecolor='w', format='png')

show()
