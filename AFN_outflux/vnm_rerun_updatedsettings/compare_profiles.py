def plot_profiles(case, shot=160300, database='../../measurements/database.hdf5',
        ylimne=(0,4e19), ylimte=(0,250), xlim=(-0.1,0.08)):
    from matplotlib.pyplot import subplots, subplots_adjust
    from h5py import File
    # Set up figure and adjust margins
    f, axs  = subplots(2, 3, figsize=(25,10))
    subplots_adjust(left=0.05, right=.98)
    # Get UEDGE normalized psi, midplane poloidal index, separatrix 
    # radial index, and R-Rsep coordinates along midplane
    psin = case.utils.psinormc()    
    ixmp = case.get('ixmp')
    iysptrx = case.get('iysptrx')
    r_rsep = case.get('rm')[ixmp,:,0] - 0.5*sum(case.get('rm')[ixmp, iysptrx, -2:])
    # Transfer shot database data to memory
    data = read_hdf5(database)[str(shot)]
    # Define plot colors for additional results to be plotted
    colors = [  'b', 'r', 'gold', 'c', 'm', 'grey', 'salmon', 
                'purple', 'olive', 'teal', 'orange'
    ]
    # List of savenames of additional results to be plotted
    saves = [
        'nomol.hdf5',
    ]
    # Helper indices for axes
    idx = [[0, 1], [1, 1], [0,2]]
    # LP profiles to plot
    LP = ['NE', 'TE', 'JSAT']
    # UEDGE variables corresponding to LP profiles
    uevar = ['ne', 'te', 'fnix']
    # Scaling factors applied to UEDGE variables to 
    # correspond to LP profiles
    uescale = [1e-6, 1/1.602e-19, 1.602e-19*1e-4]
    # Labels for LP comparisons
    ylabel = [  'Target electron density [cm**-3]',
                'Target electron temperature [eV]',
                'Target ion saturation current [part/s]']
    # Create helper variables for axes
    ax = axs[:,0]
    twinax = []
    twinax.append(ax[0].twinx())
    twinax.append(ax[1].twinx())

    """ Upstream electron density """
    # Plot experimental data
    ax[0].errorbar(
            data['midplane']['rmajor'][()]+data['midplane']['rshift'][()], 
            data['midplane']['ne'][()], 
            data['midplane']['neerr'][()],
            marker='.',
            markersize=3,
            linestyle='',
            linewidth=0.5,
            color='grey'
    )
    # Plot UEDGE predictions
    ax[0].plot(
            r_rsep[1:-1], 
            case.get('ne')[ixmp,1:-1], 
            'k-', 
            linewidth=2, 
            zorder=10
    )
    # Plot UEDGE transpor coefficient on RHS axis
    twinax[0].plot(
            r_rsep[1:-1], 
            case.get('dif_use')[ixmp,1:-1,0], 
            'k--', 
            zorder=5
    )
    # Set subplot properties
    ax[0].axvline(0, color='k', linewidth=0.5)
    ax[0].set_xlim(xlim)
    twinax[0].set_ylim(0,10)
    twinax[0].set_xlim(xlim)
    ax[0].set_ylim(ylimne)
    ax[0].set_ylabel('Midplane electron density [m**-3]')
    ax[0].set_xlabel('Normalized Psi [-]')

    """ Upstream electron temperature """
    # Plot experimental data
    ax[1].errorbar(
            data['midplane']['rmajor'][()]+data['midplane']['rshift'][()], 
            data['midplane']['Te'][()], 
            data['midplane']['Teerr'][()],
            marker='.',
            markersize=3,
            linestyle='',
            linewidth=0.5,
            color='grey'
    )
    # Plot UEDGE predictions
    ax[1].plot(
            r_rsep[1:-1],
            case.get('te')[ixmp, 1:-1]/case.get('ev'), 
            'k-', 
            linewidth=2, 
            zorder=10
    )
    # Plot UEDGE transpor coefficient on RHS axis
    twinax[1].plot(
            r_rsep[1:-1], 
            case.get('kye_use')[ixmp,1:-1], 
            'k--', 
            zorder=5
    )
    # Set subplot properties
    ax[1].axvline(0, color='k', linewidth=0.5)
    ax[1].set_xlim(xlim)
    twinax[1].set_ylim(0,3)
    twinax[1].set_xlim(xlim)
    ax[1].set_ylim(ylimte)
    ax[1].set_ylabel('Midplane electron temperature [eV]')
    ax[1].set_xlabel('Normalized Psi [-]')

    """ Plot target profiles """
    for i in range(3):
        # Define axis helper
        ax = axs[*idx[i]]
        # Plot probe data 
        ax.plot(
            data['outer_target']['PSIN'],
            data['outer_target'][LP[i]],
            '+', 
            color='grey'
        )
        # Get the UEDGE data
        var = case.get(uevar[i])[-2,1:-1]*uescale[i]
        # Account for angle of incidence if plotting Jsat
        if uevar[i] == 'fnix':
            var = var[:,0]*((case.get('btot')/case.get('bpol')[:,:,0])/\
                            case.get('sx'))[-2,1:-1]
        # Plot UEDGE data
        ax.plot(
            psin[1:-1], 
            var, 
            'k-', 
            zorder=10
        )
        # Set subplot properties
        ax.set_xlim(0.9,1.1)
        ax.set_ylabel(ylabel[i])
        ax.set_xlabel('Normalized Psi [-]')
        ax.axvline(1, color='k', linewidth=0.5)


    ax = axs[:,0]
    # Loop through requested results to be plotted
    for i in range(len(saves)):
        # Check if too many cases are defined
        if i>=len(colors):
            print("Too many cases specified, truncating at {} cases.".format(len(colors)))
            break
        # Get save file
        save = saves[i]
        # Extract data from save file        
        ne = case.tools.hdf5search(save, 'ne')[ixmp]
        kye = case.tools.hdf5search(save, 'kye_use')[ixmp]
        te = case.tools.hdf5search(save, 'te')[ixmp]/case.get('ev')
        dif = case.tools.hdf5search(save, 'dif_use')[ixmp,:,0]
        # Assuming all saves are plotted on the same grid, plot the results
        twinax[0].plot(
                r_rsep[1:-1], 
                dif[1:-1], 
                '--', 
                color = colors[i]
        )
        ax[0].plot(
                r_rsep[1:-1], 
                ne[1:-1], 
                color = colors[i]
        )
        twinax[1].plot(
                r_rsep[1:-1], 
                kye[1:-1], 
                '--', 
                color = colors[i]   
        )
        ax[1].plot(
                r_rsep[1:-1], 
                te[1:-1], 
                color = colors[i]
        )
        # Next, loop through the target data
        for j in range(3):
            # Get the target data from the save file
            var = case.tools.hdf5search(save, uevar[j])[-2,1:-1]*uescale[j]
            # Account for angle of incidence if plotting Jsat
            if uevar[j] == 'fnix':
                var = var[:,0]*((case.get('btot')/case.get('bpol')[:,:,0])/\
                        case.get('sx'))[-2,1:-1]
            # Plot save target profiles
            axs[*idx[j]].plot(
                    psin[1:-1], 
                    var, 
                    color=colors[i]
            )



def read_hdf5(file, ret = {}):
    """ Recursice function returning all HDF5 data as dict """
    from h5py import File, Dataset
    # Check if file is a filename
    if isinstance(file, str):
        # Open file for writing 
        with File(file) as f:
            # Traverse recursively
            read_hdf5(f, ret)
            # Return data dictionary
            return ret
    # file is a HDF5 data struct
    else:
        # Loop through substructures
        for key, val in file.items():
            # If the entry is data, append it to the dict
            if isinstance(val, Dataset):
                ret[key] = val[()]
            # If its a subgroup, create a dictionary entry 
            # and traverse recursively
            else:
                ret[key] = {}
                read_hdf5(val, ret[key])
    
            
