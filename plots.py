import matplotlib.pyplot as plt
import numpy as np
from Core.Calculation import Calculation
from scipy.signal import hilbert

def plotytx(f_0, f_1, tau, f_s, y_tx_n, slope):

    # Example of ideal windowed transmit signal with slope 0.5
    y_tx_n05slope, t = Calculation.generateIdealWindowedTransmitSignal(
        f_0, f_1, tau, f_s, .5)

    plt.figure()
    plt.plot(t * 1000, np.abs(hilbert(y_tx_n)), t * 1000, np.abs(hilbert(y_tx_n05slope)))
    #plt.title(
    #    'Ideal windowed transmit pulse.{:.0f}kHz - {:.0f}kHz, slope {:.3f}'
    #        .format(f_0 / 1000, f_1 / 1000, slope))
    plt.xlabel('Time (ms)')
    plt.ylabel('Envelope ()')
    plt.savefig('./Paper/Fig_ytx.png',dpi=300)


def plotfir(filter_v, f_s_dec_v, f_0, f_1):
    # The frequency response function of the filter is given by its
    # discrete time fourier transform:
    H0 = np.fft.fft(filter_v[0]["h_fl_i"])
    H1 = np.fft.fft(filter_v[1]["h_fl_i"])

    # Plot of the frequency response of the filters (power) (in dB)
    F0 = np.arange(len(H0)) * f_s_dec_v[0] / (len(H0))
    F1 = np.arange(len(H1)) * f_s_dec_v[1] / (len(H1))
    G0 = 20 * np.log10(np.abs(H0))
    # Repeat pattern for the second filter (4 times)
    F1l = np.append(F1, F1 + f_s_dec_v[1])
    F1l = np.append(F1l, F1 + 2 * f_s_dec_v[1])
    F1l = np.append(F1l, F1 + 3 * f_s_dec_v[1])
    G1 = 20 * np.log10(np.abs(H1))
    G1l = np.append(G1, G1)
    G1l = np.append(G1l, G1)
    G1l = np.append(G1l, G1)
    plt.figure()
    plt.plot(F0/1000, G0,
             F1l/1000, G1l,
             [f_0/1000, f_1/1000], [-140, -140])
    plt.xlabel('Frequency (kHz)')
    plt.ylabel('Filter gain (dB)')
    plt.xlim([0000/1000, 310000/1000])
    plt.savefig('./Paper/Fig_fir.png',dpi=300)


def plotymfn(y_mf_n):
    plt.figure()
    plt.plot(np.abs(y_mf_n))
    #plt.title('The absolute value of the filtered and decimated output signal')
    plt.xlabel('n ()')
    plt.ylabel('$y_{mf}$ ()')
    plt.savefig('./Paper/Fig_y_mf_n.png',dpi=300)


def plotACF(y_mf_auto_n):
    plt.figure()
    plt.plot(np.abs(y_mf_auto_n))
    #plt.title('The autocorrelation function of the matched filter.')
    plt.xlabel('n ()')
    plt.ylabel('$p_{tx,auto}$ ()')
    plt.savefig('./Paper/Fig_ACF.png',dpi=300)


def plotThetaPhi(theta_n, phi_n):
    # Plot angles
    fig, axs = plt.subplots(2, sharex=True)
    #fig.suptitle('Single target')
    axs[0].plot(theta_n)
    axs[0].set_ylabel(r'${\theta} (^{\circ})$')
    axs[1].plot(phi_n, color='#ff7f0e')
    axs[1].set_ylabel('$\phi (^{\circ})$')
    axs[1].set_xlabel('n ()')
    plt.savefig('./Paper/Fig_theta_phi.png',dpi=300)


def plotSingleTarget(dum_r, dum_p, dum_theta, r_t, dum_phi, phi_t, y_mf_auto_red_n):
    fig, axs = plt.subplots(2, sharex=True)
    #fig.suptitle('Single target')
    axs[0].plot(dum_r, dum_p)
    axs[0].set_ylabel('$p_{rx,e}$')
    # line1, = axs[1].plot(dum_r, dum_theta, label='$\\theta$')
    # axs[1].plot([r_t, r_t], [-2, 2])
    # line2, = axs[1].plot(dum_r, dum_phi, label='$\phi$')
    # axs[1].plot(r_t, phi_t)
    # axs[1].legend(handles=[line1, line2])
    # axs[1].set_ylabel('Angles [$\deg$]')
    axs[1].plot(dum_r, np.abs(y_mf_auto_red_n))
    axs[1].set_ylabel('$y_{mf,auto,red}$')
    axs[1].set_xlabel('Range (m)')
    plt.savefig('./Paper/Fig_singleTarget.png',dpi=300)


def plotTS(f_m, Y_pc_t_m, Y_mf_auto_red_m, Y_tilde_pc_t_m, g_theta_phi_m, TS_m):
    
    
    def text_coords(axs=None,scalex=0.9,scaley=0.9):
        xlims = axs.get_xlim()
        ylims = axs.get_ylim()
        return {'x':scalex*np.diff(xlims)+xlims[0],
                'y':scaley*np.diff(ylims)+ylims[0]}
    
    fig, axs = plt.subplots(5, sharex=True, figsize=(6.4,9))
    axs[0].plot(f_m/1000, np.abs(Y_pc_t_m))

    axs[0].set_ylabel(r'|$Y_{pc,t}$| ()', fontsize=8)
    axs[1].plot(f_m/1000, np.abs(Y_mf_auto_red_m))
    axs[1].set_ylabel(r'$|Y_{mf,auto,red}$| ()', fontsize=8)
    axs[2].plot(f_m/1000, np.abs(Y_tilde_pc_t_m))
    axs[2].set_ylabel(r'|$\tilde{Y}_{pc,t}$| ()', fontsize=8)
    axs[3].plot(f_m/1000,g_theta_phi_m)  # weird gain might be tracked down to  xml['angle_offset_alongship'] and xml['angle_offset_alongship']
    axs[3].set_ylabel('Transducer gain (dB)')
    axs[4].plot(f_m/1000, TS_m)
    axs[4].set_xlabel('f (kHz)')
    axs[4].set_ylabel('TS (dB re $1m^2$)')

    scalex = [0.02,0.02,0.02,0.02,0.02]
    scaley = [0.75,0.75,0.75,0.75,0.75]
    labels = ['(a)','(b)','(c)','(d)','(e)']

    # f,ax = plt.subplots(2,2)
    for sx,sy,a,l in zip(scalex,scaley,np.ravel(axs),labels):
        a.text(s=l,**text_coords(axs=a,scalex=sx,scaley=sy))
    
    plt.savefig('./Paper/Fig_TS.png',dpi=300)

    # Store TS(f) and f for further analysis
    TSfOut = np.stack((f_m,TS_m), axis=0)
    np.save('TSf.npy',TSfOut)


def plotSvf(f_m,Sv_m_n,svf_range):
    plt.figure()
    _f = f_m / 1000
    plt.imshow(Sv_m_n, extent=[_f[0], _f[-1], svf_range[-1], svf_range[0]], origin='upper',
               interpolation=None)
    cb = plt.colorbar()
    cb.set_label('Sv (dB re 1 m$^1$)')
    #plt.title('Echogram [Sv]')
    plt.xlabel('Frequency (kHz)')
    plt.ylabel('Range (m)')
    plt.axis('auto')
    plt.savefig('./Paper/Fig_Sv_m_n.png',dpi=300)

    # # Plot Sv(f) in one depth in the middle of layer
    # plt.figure()
    # indices=np.where(np.logical_and(svf_range>=15, svf_range<=34))
    # Sv=[]
    # plt.plot(Sv_m_n[int(len(indices[0]) / 2) - 1,])
    # plt.title('Sv(f) at one depth')
    # plt.xlabel('Frequency [kHz]')
    # plt.ylabel('Sv')
    # plt.grid()

    indices = np.where(np.logical_and(svf_range >= 15, svf_range <= 34))
    # returns indices for depth layer of school
    Sv = []
    for i in range(len(f_m)):
        sv = 10 ** (Sv_m_n[indices, i] / 10)
        sv = sv.mean()
        Sv.append(10 * np.log10(sv))

    # plot a Sv(f) over school
    #from matplotlib.pyplot import figure, show, subplots_adjust, get_cmap
    #fig1 = figure()
    plt.figure()
    plt.plot(f_m / 1000, Sv)  # values are for some reason to low, add ~17dB
    #plt.title('Sv(f) averaged over school depths')
    plt.xlabel('Frequency (kHz)')
    plt.ylabel('Sv (dB re 1 m$^1$)')
    plt.grid()
    plt.savefig('./Paper/Fig_Sv_avg.png',dpi=300)
    # Store Sv(f) and f for further analysis
    SvfOut = np.concatenate((f_m[np.newaxis],Sv_m_n), axis=0)
    np.save('Svf.npy',SvfOut)
