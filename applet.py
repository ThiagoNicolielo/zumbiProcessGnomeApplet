#!/usr/bin/env python
### NORMAL IMPORTS
import sys, gtk, pygtk, gnomeapplet, gobject, subprocess

pygtk.require('2.0')

#### CREATE A MENU WITH XML
#def create_menu(applet):
#    xml = """
#    <popup name="button3">
#        <menuitem name="Item 1" verb="Detalhes" label="_Detalhes...."
#            pixtype = "stock" pixname="gtk-properties"/>
#    </popup>
#    """
#    verbs = [('Detalhes',show_detalhes)]
#    applet.setup_menu(xml, verbs, None)

#### WHAT HAPPENS WHEN MENU ITEM IS CLICKED
#def show_detalhes(*arguments):
#    print(arguments)

def kill(applet):
    processosZumbis = verificaProcessosZumbis()
    idProcessos = []
    subprocess.Popen('touch /home/28519192882/applet/log.txt', shell=True, stdout=subprocess.PIPE).communicate()[0].split('\n')
    for p in processosZumbis:
        idProcesso = p.split(' ')[1]
#        minutosExecutando, segundosExecutando = p.split(' ')[9].split(':')
        subprocess.Popen('ps -p ' + idProcesso + ' o user,pid,pcpu,pmem,vsz,rss,tty,stat,start,time,command >> /home/28519192882/applet/log.txt', shell=True, stdout=subprocess.PIPE).communicate()[0].split('\n')
#        subprocess.Popen('echo ' + minutosExecutando + ' : ' + segundosExecutando + ' >> /home/28519192882/applet/log.txt', shell=True, stdout=subprocess.PIPE).communicate()[0].split('\n')
        subprocess.Popen('kill -9 ' + idProcesso, shell=True, stdout=subprocess.PIPE)
    print("killed them all")

def verificaProcessosZumbis():
    processosZumbis = []
    processos = subprocess.Popen("ps -eo stat,pid,time,command | grep 'firefox -foreground' | tr -s ' ' | grep -v grep", shell=True, stdout=subprocess.PIPE).communicate()[0].split('\n')
#    processos = subprocess.Popen("ps aux | grep 'firefox -foreground' | tr -s ' ' | grep -v grep", shell=True, stdout=subprocess.PIPE).communicate()[0].split('\n')
#    processos = subprocess.Popen("ps aux | grep 'firefox -foreground' | tr -s ' '", shell=True, stdout=subprocess.PIPE).communicate()[0].split('\n')
    processos.remove('')
    if processos.__len__() > 0:
        print('>>>processos[0]: ' + processos[0])
        print('processos.__len__() :' + str(processos.__len__()) + '\n')
        print('=================================\n')
    for p in processos:
        print('\n>>>iteracao p de processos: ' + p)
#        print('p.__len__() :' + str(p.__len__()))
#        print('oi ' + p.split(' ')[9] + '\n')
#        processosZumbis.append(p)
#        print('>>>processosZumbi[0]: ' + processosZumbis[0])
#        print('processosZumbis.__len__() :' + str(processosZumbis.__len__()))
        try:
            horasExecutando, minutosExecutando, segundosExecutando = p.split(' ')[2].split(':')
            print ("segundosExecutando: " + segundosExecutando)
            if ( (int(horasExecutando)*60*60 + int(minutosExecutando)*60 + int(segundosExecutando)) >= 3 ) :
#                processosZumbis.append(p)
#                print('\n>>>processosZumbis a mais de 1 minuto executando: ' + p)
#                print('p.__len__() :' + str(p.__len__()) + '\n')
                if ( p.split(' ')[0] == "Rl" ):
                    print("p.split(' ')[1]: " + p.split(' ')[1])
                    processosZumbis.append(p)
        except:
            pass
    print('====================================')
    print('====================================')
    return processosZumbis

def numeroZumbis(applet):
    processosZumbis = verificaProcessosZumbis()
    if processosZumbis.__len__() > 0:
        return processosZumbis.__len__()
    else:
        return 0

def atualiza(applet):
    print('aaa')
    applet.hbox.remove(applet.totalZumbisLabel)
    applet.hbox.remove(applet.botao)

    applet.totalZumbisLabel.set_text(str(numeroZumbis(applet)))
    applet.hbox.pack_start(applet.totalZumbisLabel)

    if (numeroZumbis(applet) > 0):
        applet.hbox.pack_start(applet.botao)

    applet.show_all()
    gobject.timeout_add(1000, atualiza, applet)

### WHERE IT ALL HAPPENS
def applet_factory(applet, iid):
    # CREATE THE XML MENU
#    create_menu(applet)
    # CREATE AN EVENT FOR CLICKING THE APPLET
#    applet.connect('button-press-event',button_press)

    applet.label = gtk.Label("Zumbis: ")

    applet.totalZumbisLabel = gtk.Label("0")

    #Cria o botao, e muda sua cor para vermelho
    applet.botao = gtk.Button("Kill")
    #make a gdk.color for red
    map = applet.botao.get_colormap() 
    color = map.alloc_color("red")
    #copy the current style and replace the background
    style = applet.botao.get_style().copy()
    style.bg[gtk.STATE_NORMAL] = color
    style.bg[gtk.STATE_ACTIVE] = color
    style.bg[gtk.STATE_PRELIGHT] = color
    #set the button's style to the one you created
    applet.botao.set_style(style)

    applet.botao.connect("clicked",kill)

    applet.hbox = gtk.HBox()
    applet.hbox.pack_start(applet.label)
    applet.hbox.pack_start(applet.totalZumbisLabel)
    applet.add(applet.hbox)

    # SHOW IT!
    applet.show_all()

    gobject.timeout_add(1000, atualiza, applet)

    # DEBUG EVENT
    print('Factory started')

    return True

#### CREATE A DIALOG TO POP UP WHEN APPLET IS CLICKED
#def test(*arguments):
#    print(arguments)
#    dia = gtk.Dialog("Mensagem",None,gtk.DIALOG_MODAL)
#    lbl = gtk.Label("Esta eh uma mensagem")
#    dia.vbox.pack_start(lbl)
#    lbl.show()
#    dia.run()
#    dia.connect("destroy",dia.destroy)

#### HANDLE THE APPLET CLICK
#def button_press(button, event):
#    # LEFT BUTTON ACTIVATES THE CUSTOM MENU
#    if event.button == 1:
#        print "button 1"
#        # CREATE A CUSTOM MENU
#        menu = gtk.Menu()
#        item = gtk.MenuItem("Oi")
#        item.show()
#        # CONNECT THIS MENU ITEM TO THE DIALOG
#        item.connect("activate",test,"Oi")
#        menu.append(item)
#        # FINISH THE POPUP MENU
#        menu.popup(None, None, None, event.button, event.time, None)
#    # RIGHT BUTTON ACTIVATES THE STANDARD MENU
#    elif event.button == 2:
#        # DEBUG
#        print "button 2"#

### STANDARD ENTRY
if __name__ == '__main__':
    # DEBUG
    print('Starting factory')
    # RUN THE APPLET AS A GTK WINDOW IN DEBUG (-d) MODE
    if len(sys.argv) > 1 and sys.argv[1] == '-d':
        mainWindow = gtk.Window()
        mainWindow.set_title('Applet window')
        mainWindow.connect('destroy',gtk.main_quit)
        applet = gnomeapplet.Applet()
        applet_factory(applet, None)
        applet.reparent(mainWindow)
        mainWindow.show_all()
        gtk.main()
        sys.exit()
    # LET GNOME TAKE CARE OF IT AS AN APPLET
    else:
        gnomeapplet.bonobo_factory('OAFIID:GNOME_PythonAppletSample_Factory',
            gnomeapplet.Applet.__gtype__,
            'Sample Applet', '0.1',
            applet_factory)
