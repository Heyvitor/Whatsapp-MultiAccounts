from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtWebEngineWidgets import *
from PyQt5.QtWebEngineCore import *
from PyQt5.QtNetwork import *
from PyQt5.QtGui import QIcon, QPixmap
import sys
import os
import shutil
import time

# Inicialização global do WebEngine
os.environ["QTWEBENGINE_CHROMIUM_FLAGS"] = "--no-sandbox --disable-web-security"
os.environ["QTWEBENGINE_DISABLE_SANDBOX"] = "1"

class CustomWebEnginePage(QWebEnginePage):
    def __init__(self, profile, parent=None):
        super().__init__(profile, parent)
        
    def userAgentForUrl(self, url):
        # User Agent específico do Firefox
        return "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:123.0) Gecko/20100101 Firefox/123.0"
        
    def javaScriptConsoleMessage(self, level, message, lineNumber, sourceID):
        pass

class InstanceNameDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle('Nova Instância Firefox')
        self.setFixedSize(300, 100)
        
        layout = QVBoxLayout()
        
        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText('Digite o nome da instância')
        layout.addWidget(self.name_input)
        
        buttons = QHBoxLayout()
        ok_button = QPushButton('Criar')
        cancel_button = QPushButton('Cancelar')
        
        ok_button.clicked.connect(self.accept)
        cancel_button.clicked.connect(self.reject)
        
        buttons.addWidget(ok_button)
        buttons.addWidget(cancel_button)
        layout.addLayout(buttons)
        
        self.setLayout(layout)
        
        # Estilo Dark
        self.setStyleSheet("""
            QDialog {
                background-color: #1a1a1a;
                color: white;
            }
            QLineEdit {
                padding: 5px;
                border-radius: 3px;
                background-color: #2a2a2a;
                color: white;
                border: 1px solid #3a3a3a;
            }
            QPushButton {
                background-color: #128C7E;
                color: white;
                border: none;
                padding: 5px 15px;
                border-radius: 3px;
            }
            QPushButton:hover {
                background-color: #25D366;
            }
        """)

class WhatsAppInstanceWidget(QWidget):
    def __init__(self, name, parent=None, delete_callback=None):
        super().__init__(parent)
        layout = QHBoxLayout()
        layout.setContentsMargins(2, 2, 2, 2)
        layout.setSpacing(2)
        
        # Apenas ícone com tooltip
        icon_label = QLabel("📱")
        icon_label.setStyleSheet("""
            font-size: 16px;
            color: #aaa;
            padding: 5px;
        """)
        icon_label.setToolTip(name)
        layout.addWidget(icon_label)
        
        # Botão de deletar pequeno
        delete_button = QPushButton("×")
        delete_button.setFixedSize(16, 16)
        delete_button.setStyleSheet("""
            QPushButton {
                background-color: transparent;
                color: #666;
                border: none;
                font-size: 14px;
                font-weight: bold;
                padding: 0px;
            }
            QPushButton:hover {
                color: #ff4444;
            }
        """)
        if delete_callback:
            delete_button.clicked.connect(lambda: delete_callback(name))
        
        layout.addWidget(delete_button)
        self.setLayout(layout)
        self.setFixedHeight(30)
        self.setFixedWidth(50)
        
        self.setStyleSheet("""
            QWidget {
                background-color: #2a2a2a;
                border-radius: 3px;
                margin: 1px;
            }
            QWidget:hover {
                background-color: #3a3a3a;
            }
        """)

class WhatsAppManager(QMainWindow):
    def __init__(self):
        super().__init__()
        self.instances = []
        self.current_profile = 0
        self.current_tabs = {}
        
        self.base_profile_path = os.path.join(os.path.expanduser("~"), "Documents", "WhatsAppProfiles")
        if not os.path.exists(self.base_profile_path):
            os.makedirs(self.base_profile_path)
        
        self.instances_file = os.path.join(self.base_profile_path, "saved_instances.txt")
        
        # Configurações atualizadas para áudio e microfone
        os.environ["QTWEBENGINE_CHROMIUM_FLAGS"] = "--disable-web-security --use-fake-ui-for-media-stream --enable-features=WebRTCPipeWireCapturer --autoplay-policy=no-user-gesture-required"
        
        self.setupUI()
        self.load_saved_instances()

    def setupUI(self):
        self.setWindowTitle('WhatsApp Multi-Instância')
        self.setGeometry(100, 100, 1400, 800)
        
        # Widget principal
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        layout = QHBoxLayout(main_widget)
        layout.setSpacing(0)
        layout.setContentsMargins(0, 0, 0, 0)
        
        # Painel esquerdo
        left_panel = QWidget()
        left_panel.setFixedWidth(60)
        left_layout = QVBoxLayout(left_panel)
        left_layout.setContentsMargins(3, 3, 3, 3)
        
        # Botão de criar
        create_button = QPushButton("+")
        create_button.setFixedSize(30, 30)
        create_button.clicked.connect(self.create_instance)
        
        button_container = QHBoxLayout()
        button_container.addStretch()
        button_container.addWidget(create_button)
        button_container.addStretch()
        left_layout.addLayout(button_container)
        
        # Lista de instâncias
        self.instance_list = QListWidget()
        self.instance_list.itemClicked.connect(self.switch_instance)
        left_layout.addWidget(self.instance_list)
        left_panel.setLayout(left_layout)
        
        # Painel direito
        self.tab_widget = QTabWidget()
        self.tab_widget.setTabsClosable(True)
        self.tab_widget.tabCloseRequested.connect(self.delete_instance)
        
        # Adicionar painéis ao layout
        layout.addWidget(left_panel)
        layout.addWidget(self.tab_widget, 1)
        
        # Aplicar estilos
        self.apply_styles()

    def create_instance(self):
        dialog = InstanceNameDialog(self)
        if dialog.exec_():
            instance_name = dialog.name_input.text().strip()
            if not instance_name:
                QMessageBox.warning(self, "Erro", "Nome da instância não pode estar vazio!")
                return
                
            if instance_name in self.instances:
                QMessageBox.warning(self, "Erro", "Uma instância com este nome já existe!")
                return
            
            try:
                self.create_instance_with_name(instance_name)
                self.save_instances()
            except Exception as e:
                QMessageBox.critical(self, "Erro", f"Erro ao criar instância: {str(e)}")

    def create_instance_with_name(self, instance_name):
        web_view = QWebEngineView()
        profile = QWebEngineProfile(instance_name, web_view)
        profile.setPersistentStoragePath(os.path.join(self.base_profile_path, instance_name))
        profile.setHttpUserAgent("Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:123.0) Gecko/20100101 Firefox/123.0")
        
        # Configurações corrigidas para áudio e microfone
        settings = web_view.settings()
        settings.setAttribute(QWebEngineSettings.JavascriptEnabled, True)
        settings.setAttribute(QWebEngineSettings.LocalStorageEnabled, True)
        settings.setAttribute(QWebEngineSettings.WebRTCPublicInterfacesOnly, True)
        settings.setAttribute(QWebEngineSettings.LocalContentCanAccessRemoteUrls, True)
        settings.setAttribute(QWebEngineSettings.AllowRunningInsecureContent, True)
        settings.setAttribute(QWebEngineSettings.PlaybackRequiresUserGesture, False)
        settings.setAttribute(QWebEngineSettings.JavascriptCanAccessClipboard, True)
        settings.setAttribute(QWebEngineSettings.ScreenCaptureEnabled, True)
        settings.setAttribute(QWebEngineSettings.AutoLoadImages, True)
        
        # Página personalizada com permissões
        page = CustomWebEnginePage(profile, web_view)
        web_view.setPage(page)
        
        # Configurar permissões de mídia
        page.featurePermissionRequested.connect(self.handle_permission_request)
        
        web_view.setUrl(QUrl("https://web.whatsapp.com"))
        
        self.tab_widget.addTab(web_view, instance_name)
        self.instances.append(instance_name)
        self.current_tabs[instance_name] = web_view
        
        # Adicionar à lista com ícone
        item = QListWidgetItem(self.instance_list)
        instance_widget = QWidget()
        layout = QHBoxLayout(instance_widget)
        layout.setContentsMargins(2, 2, 2, 2)
        
        icon_label = QLabel("🦊")
        icon_label.setStyleSheet("font-size: 16px; color: #ff9500;")
        layout.addWidget(icon_label)
        
        delete_button = QPushButton("×")
        delete_button.setFixedSize(16, 16)
        delete_button.setStyleSheet("""
            QPushButton {
                background-color: transparent;
                color: #666;
                border: none;
                font-size: 14px;
                font-weight: bold;
            }
            QPushButton:hover {
                color: #ff4444;
            }
        """)
        delete_button.clicked.connect(lambda: self.confirm_delete_instance(instance_name))
        layout.addWidget(delete_button)
        
        instance_widget.setLayout(layout)
        item.setSizeHint(instance_widget.sizeHint())
        self.instance_list.setItemWidget(item, instance_widget)

    def confirm_delete_instance(self, instance_name):
        reply = QMessageBox.question(
            self,
            'Confirmar Exclusão',
            f'Deseja realmente excluir a instância "{instance_name}"?\nTodos os dados serão perdidos.',
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )
        
        if reply == QMessageBox.Yes:
            self.delete_instance_by_name(instance_name)

    def delete_instance_by_name(self, instance_name):
        try:
            # Encontrar e remover a aba
            for i in range(self.tab_widget.count()):
                if self.tab_widget.tabText(i) == instance_name:
                    web_view = self.tab_widget.widget(i)
                    
                    if web_view:
                        # Desconectar sinais e parar carregamentos
                        web_view.page().profile().deleteLater()
                        web_view.page().deleteLater()
                        web_view.stop()
                        web_view.setUrl(QUrl("about:blank"))
                        
                        # Remover a aba antes de deletar o widget
                        self.tab_widget.removeTab(i)
                        web_view.deleteLater()
                    break
            
            # Remover da lista visual
            for i in range(self.instance_list.count()):
                item = self.instance_list.item(i)
                widget = self.instance_list.itemWidget(item)
                if widget and widget.findChild(QLabel).text() == "🦊":
                    self.instance_list.takeItem(i)
                    break
            
            # Remover das listas de controle
            if instance_name in self.instances:
                self.instances.remove(instance_name)
            if instance_name in self.current_tabs:
                del self.current_tabs[instance_name]
            
            # Remover arquivos do perfil de forma segura
            profile_path = os.path.join(self.base_profile_path, instance_name)
            if os.path.exists(profile_path):
                def delete_profile():
                    try:
                        # Aguardar um pouco para garantir que os recursos foram liberados
                        time.sleep(0.5)
                        if os.path.exists(profile_path):
                            shutil.rmtree(profile_path, ignore_errors=True)
                    except Exception as e:
                        print(f"Erro ao deletar perfil: {e}")
                
                # Executar deleção em thread separada
                QTimer.singleShot(1000, delete_profile)
            
            # Atualizar lista salva
            self.save_instances()
            
            # Forçar atualização da interface
            QApplication.processEvents()
            
        except Exception as e:
            print(f"Erro ao deletar instância: {e}")

    def save_instances(self):
        try:
            with open(self.instances_file, 'w') as f:
                for instance in self.instances:
                    f.write(f"{instance}\n")
        except Exception as e:
            print(f"Erro ao salvar instâncias: {e}")

    def load_saved_instances(self):
        try:
            if os.path.exists(self.instances_file):
                with open(self.instances_file, 'r') as f:
                    saved_instances = f.read().splitlines()
                    for instance_name in saved_instances:
                        if instance_name.strip():
                            self.create_instance_with_name(instance_name)
        except Exception as e:
            print(f"Erro ao carregar instâncias: {e}")

    def switch_instance(self, item):
        try:
            index = self.instance_list.row(item)
            if index >= 0 and index < self.tab_widget.count():
                self.tab_widget.setCurrentIndex(index)
        except Exception as e:
            print(f"Erro ao trocar instância: {e}")

    def delete_instance(self, index):
        try:
            if 0 <= index < self.tab_widget.count():
                web_view = self.tab_widget.widget(index)
                profile_name = self.tab_widget.tabText(index)
                
                if web_view:
                    # Parar carregamentos e limpar
                    web_view.stop()
                    web_view.setUrl(QUrl("about:blank"))
                    
                    # Limpar perfil Firefox
                    profile = web_view.page().profile()
                    if profile:
                        profile.clearHttpCache()
                        profile.clearAllVisitedLinks()
                    
                    web_view.deleteLater()
                
                # Remover da interface
                self.tab_widget.removeTab(index)
                self.instance_list.takeItem(index)
                
                # Remover das listas
                if profile_name in self.instances:
                    self.instances.remove(profile_name)
                if profile_name in self.current_tabs:
                    del self.current_tabs[profile_name]
                
                # Remover perfil Firefox
                profile_path = os.path.join(self.base_profile_path, profile_name)
                if os.path.exists(profile_path):
                    try:
                        shutil.rmtree(profile_path)
                    except:
                        pass
                
        except Exception as e:
            print(f"Erro ao deletar instância Firefox: {e}")

    def apply_styles(self):
        self.setStyleSheet("""
            QMainWindow, QWidget {
                background-color: #1a1a1a;
                color: #ffffff;
            }
            QPushButton {
                background-color: #128C7E;
                color: white;
                border-radius: 15px;
                font-size: 20px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #25D366;
            }
            QListWidget {
                background-color: #2a2a2a;
                border: none;
            }
            QTabWidget::pane {
                border: none;
                background-color: #1a1a1a;
            }
            QTabBar::tab {
                background-color: #2a2a2a;
                color: #aaaaaa;
                padding: 8px 15px;
                margin: 0px 2px;
                border-radius: 3px 3px 0 0;
            }
            QTabBar::tab:selected {
                background-color: #3a3a3a;
                color: #ffffff;
            }
        """)

    def closeEvent(self, event):
        try:
            # Apenas salvar o estado das instâncias
            self.save_instances()
            
            # Limpar recursos de forma segura
            for instance_name in list(self.current_tabs.keys()):
                web_view = self.current_tabs[instance_name]
                if web_view:
                    web_view.stop()
                    web_view.setUrl(QUrl("about:blank"))
                    web_view.page().profile().deleteLater()
                    web_view.page().deleteLater()
                    web_view.deleteLater()
            
            event.accept()
            
        except Exception as e:
            print(f"Erro ao fechar aplicação: {e}")
            event.accept()

    def handle_permission_request(self, origin, feature):
        # Aceitar automaticamente permissões de mídia
        if feature in [QWebEnginePage.MediaAudioCapture, 
                      QWebEnginePage.MediaVideoCapture, 
                      QWebEnginePage.MediaAudioVideoCapture,
                      QWebEnginePage.DesktopVideoCapture,
                      QWebEnginePage.DesktopAudioVideoCapture]:
            self.sender().setFeaturePermission(origin, feature, QWebEnginePage.PermissionGrantedByUser)
        else:
            self.sender().setFeaturePermission(origin, feature, QWebEnginePage.PermissionDeniedByUser)

if __name__ == '__main__':
    try:
        app = QApplication(sys.argv)
        
        # Configurar proxy
        proxy = QNetworkProxy()
        proxy.setType(QNetworkProxy.NoProxy)
        QNetworkProxy.setApplicationProxy(proxy)
        
        # Criar e mostrar janela
        window = WhatsAppManager()
        window.show()
        
        sys.exit(app.exec_())
    except Exception as e:
        print(f"Erro na inicialização: {e}")
