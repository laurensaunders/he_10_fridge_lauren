import time
import powersupply as ps
import wx
import gettemp
import getslope


def run():
    for name in ps_names:
        name.ps.set_voltage(0.0)
        wx.PostEvent(parent, messageevent(message=('Setting %s to 0V.' % name)))

    wx.PostEvent(parent, messageevent(message='Waiting for switches to cool.'))
    while gettemp.gettemp(datafile_name, 'He4 IC Switch') > 8 or \
        gettemp.gettemp(datafile_name, 'He3 IC Switch') > 13 or \
        gettemp.gettemp(datafile_name, 'He UC Switch') > 8:
        if waitforkill(1, killevent): return

    # Heat 4HE IC pump first, then do the other He3 pumps next
    wx.PostEvent(parent, messageevent(message='Turning on 4He IC Pump to -25 V.'))
    He4p.ps.set_voltage(-25)
    if waitforkill(2, killevent): return

    wx.Postevent(parent, messageevent(message='Waiting for 4He IC Pump to reach 33K.'))
    while gettemp.gettemp(datafile_name, 'He4 IC Pump') < 33:
        if waitforkill(2, killevent): return

    wx.PostEvent(parent, messageevent(message='Lowering 4He IC Pump voltage to -4.5V.'))
    He4p.ps.set_voltage(-4.5)

    #Heat 3He pumps
    wx.PostEvent(parent, messageevent(message='Turning on 3He IC Pump to +25 V.'))
    He3ICp.ps.set_voltage(25)
    if waitforkill(2, killevent): return

    wx.PostEvent(parent, messageevent(message='Turning on 3He UC Pump to +25 V.'))
    He3UCp.ps.set_voltage(-25)
    if waitforkill(2, killevent): return

    wx.PostEvent(parent, messageevent(message='Waiting for all switches to be <8K, and 3He pumps to be >47K'))
    isHe3ICHigh, isHe3UCHigh = True, True
    while gettemp.gettemp(datafile_name, 'He4 IC Switch') > 8 or gettemp.gettemp(datafile_name, 'He3 IC Swtich') > 8 or gettemp.gettemp(datafile_name, 'He3 UC Swtich') > 8 or isHe3ICHigh or isHe3UCHigh:
        if waitforkill(2, killevent): return

        # TODO: Don't hardcode in thermometer names, lookup from logger python modules (AJA)
        if gettemp.gettemp(datafile_name, 'He3 IC Pump')> 47 and isHe3ICHigh==True:
            wx.PostEvent(parent, messageevent(message='Lowering 3He IC Pump voltage to 4.55 V.'))
            He3ICp.ps.set_voltage(4.55)
            if waitforkill(2, killevent): return
            isHe3ICHigh = False

        if gettemp.gettemp(datafile_name, 'He3 UC Pump') > 47 and isHe3UCHigh==True:
            wx.PostEvent(parent, messageevent(message='Lowering 3He UC Pump voltage to -6.72V.'))
            He3UCp.ps.set_voltage(-6.72)
            if waitforkill(2, killevent): return
            isHe3UCHigh = False

    wx.PostEvent(parent, messageevent(message='Waiting for mainplate to settle'))

    #Checks to see if Mainplate has settled by checking the last 10 slopes in the datafile.
    #wait 10 minutes before checking
    if waitforkill(600, killevent): return

    while getslope.getslope(datafile_name, 'mainplate', 60) > 0.001:
        if waitforkill(10, killevent): return

    wx.PostEvent(parent, messageevent(message='Mainplate has settled')
    wx.PostEvent(parent, messageevent(message='Turning off 4He IC pump and turning on switch'))
    He4p.ps.set_voltage(0)
    He4s.ps.set_voltage(5)

    wx.PostEvent(parent, messageevent(message='Waiting for heat exchanger to increase suddenly'))
    if waitforkill(1200, killevent): return
    while getslope.getslope(datafile_name, 'HEX', 60) < 0.003:
        if waitforkill(10, killevent): return

    wx.PostEvent(parent, messageevent(message='HEX has started increasing'))
    wx.PostEvent(parent, messageevent(message='Now turning off 3He IC Pump and turning on switch'))
    He3ICp.ps.set_voltage(0)
    He3ICs.ps.set_voltage(5)

    wx.PostEvent(parent, messageevent(message='Waiting for heat exchanger and mainplate to settle'))
    if waitforkill(600, killevent): return
    while abs(getslope.getslope(datafile_name, 'mainplate', 60)) > 0.001:
        if waitforkill(10, killevent): return

    wx.PostEvent(parent, messageevent(message='Now turning off 3He UC Pump and turning on switch'))
    He3UCp.ps.set_voltage('3He UC pump', 0)
    He3UCs.ps.set_voltage('3He UC switch', 5)

    if waitforkill(600, killevent): return

    wx.PostEvent(parent, messageevent(message='Cycle is complete'))

if __name__ == '__main__':
    # TODO: Add this [AJA]
    # when running as a standalone script, redirect messageevents to the
    # terminal via a dummy parent object
    print 'Starting autocycle...'
