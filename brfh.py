#!/usr/bin/python
#-*- coding: UTF-8 -*-

# BRFH - Batch Renamer From Hell - is a tool to rename a large amount of files, indexing them
# by numbers.
# Copyright (C) 2007 Flávio Amieiro <amieiro.flavio@gmail.com>
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; version 2 dated June, 1991.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Library General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, see <http://www.gnu.org/licenses/>.
#
# If you find any bugs or have any suggestions email: amieiro.flavio@gmail.com

import os
import sys

try:
    import pygtk
    pygtk.require('2.0')
except:
    pass

try:
    import gtk
    import gtk.glade
except:
    sys.exit(1)

class BatchRename:

    def __init__(self):
        """inicializa a classe BatchRename - a principal do programa"""
        self.gladefile = 'brfh.glade'
        self.wTree = gtk.glade.XML(self.gladefile, 'main_window') #aqui eu crio a 'árvore de widgets', determinando 'main_window' como a raiz

        #crio dicionário com os sinais e suas respectivas funções e depois os conecto:
        dic = {'on_main_window_destroy': gtk.main_quit,
                'on_select_all_clicked': self.selectAll,
                'on_rename_clicked': self.rename,
                'on_about_clicked': self.aboutDlg}
        self.wTree.signal_autoconnect(dic)

        #pegaremos alguns widgets aqui:
        self.FileChooser = self.wTree.get_widget('FileChooser')
        self.Filename_en = self.wTree.get_widget('new_filename_en')
        self.new_filename_label = self.wTree.get_widget('new_filename_label')

    def selectAll(self, widget):
        """Seleciona todos os arquivos da pasta atual"""
        self.FileChooser.select_all()
        print 'Select All'

    def rename(self, widget):
        """Essa função é o burro de carga do programa. Faz todo o trabalho"""
        new_filename = self.Filename_en.get_text() #pega o novo nome para os arquivos a partir da entrada do usuário.
        #resolvi não aceitar que o usuário deixe aquele campo em branco (assim o programa renomearia todos os arquivos apenas com números.
        if new_filename == '':
            dTree = gtk.glade.XML(self.gladefile, 'empty_dlg')
            dlg = dTree.get_widget('empty_dlg')
            dlg.run()
            dlg.destroy()
            self.new_filename_label.set_text('Coloca o novo nome aí do lado...')
        else:
            files_to_change = self.FileChooser.get_filenames()
            if files_to_change:#Se nenhum arquivo estiver selecionado, não vai rodar. Assim evito erros do tipo 'no such file or directory'
                response = self.showWarningDlg(len(files_to_change)) #Mostra o diálogo de aviso, e espera a resposta do usuário:
                if response == gtk.RESPONSE_OK: #só vai renomear se for OK.
                    count = 1
                    for file in files_to_change:
                        file_long = os.path.realpath(file)
                        root, ext = os.path.splitext(file_long)
                        directory = os.path.dirname(root)
                        current_name = '%s%03d%s' % (new_filename, count, ext)
                        current_name = os.path.join(directory, current_name)
                        os.rename(file_long, current_name)
                        count = count + 1
                    print 'Done'
                elif response == gtk.RESPONSE_CANCEL:
                    pass

    def showWarningDlg(self, n):
        """ Mostra um diálogo com o número de arquivos que serão modificados e avisa
            que a operação não pode ser desfeita, perguntando se deve prosseguir.
            Retorna a resposta (gtk.RESPONSE_OK ou gtk.RESPONSE_CANCEL) do usuário"""
        dTree = gtk.glade.XML(self.gladefile, 'warning_dlg')
        dlg = dTree.get_widget('warning_dlg')
        warning_label = dTree.get_widget('warning_label')
        if n == 1:
            warning_label.set_text('%d arquivo será renomeado. Esta ação não poderá ser desfeita.\n Posso continuar?' % (n))
        else:
            warning_label.set_text('%d arquivos serão renomeados. Esta ação não poderá ser desfeita.\n Posso continuar?' % (n))
        response = dlg.run()
        #print dlg.run()
        dlg.destroy()
        return response

    def aboutDlg(self, widget):
        """Mostra o diálogo de 'Sobre' do programa, inclusive com a licensa"""
        dTree = gtk.glade.XML(self.gladefile, 'about_dlg')
        dlg = dTree.get_widget('about_dlg')
        dlg.run()
        dlg.destroy()


#loop principal. Só roda se o programa estiver sozinho, não se ele for importado (como um módulo).
if __name__ == '__main__':
    batchRename = BatchRename()
    gtk.main()
