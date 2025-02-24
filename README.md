# WhatsApp Multi-Instância

Um gerenciador de múltiplas instâncias do WhatsApp Web com interface moderna e tema dark.

## 📋 Características

- Múltiplas instâncias do WhatsApp Web
- Interface moderna com tema dark
- Suporte a áudio e microfone
- Salvamento automático das instâncias
- Perfis independentes
- Design minimalista
- Compatível com chamadas de voz/vídeo

## 🚀 Requisitos

- Python 3.6+
- PyQt5
- PyQtWebEngine

## 📦 Instalação

1. Instale as dependências: pip install PyQt5 PyQtWebEngine
2. Clone o repositório ou baixe o código fonte
3. Execute o aplicativo: python new.py


## 💻 Como Usar

1. Inicie o aplicativo
2. Clique no botão "+" para criar uma nova instância
3. Digite um nome para a instância
4. Escaneie o QR Code com seu WhatsApp
5. Repita o processo para criar mais instâncias

## 🔧 Funcionalidades

- **Criar Instância**: Botão "+" no painel esquerdo
- **Excluir Instância**: Botão "×" ao lado de cada instância
- **Trocar Instância**: Clique no ícone da instância desejada
- **Salvar Instâncias**: Automático
- **Áudio/Microfone**: Permissões automáticas

## 📂 Armazenamento

- Perfis salvos em: `~/Documents/WhatsAppProfiles/`
- Lista de instâncias: `saved_instances.txt`
- Cada instância tem sua própria pasta

## 🎨 Interface

- Tema Dark
- Painel lateral compacto
- Ícone do Firefox para cada instância
- Design minimalista e intuitivo
- Abas organizadas

## ⚙️ Configurações

- User Agent do Firefox
- Suporte a WebRTC
- Configurações otimizadas para mídia
- Permissões automáticas para áudio/vídeo
- Armazenamento persistente

## 🔒 Segurança

- Instâncias isoladas
- Perfis independentes
- Sem compartilhamento de dados
- Limpeza segura ao excluir

## ⚠️ Observações

- Uma instância por número de WhatsApp
- Necessário escanear QR Code para cada instância
- Mantenha o aplicativo atualizado
- Requer conexão com a internet

## 🐛 Solução de Problemas

1. **Erro ao criar instância**:
   - Verifique a conexão com a internet
   - Reinicie o aplicativo

2. **Áudio não funciona**:
   - Verifique as permissões do sistema
   - Confirme se o dispositivo de áudio está funcionando

3. **Instância não salva**:
   - Verifique permissões da pasta
   - Aguarde a sincronização completa

## 📝 Licença

Este projeto está sob a licença MIT.

## 👨‍💻 Desenvolvimento

- Desenvolvido com PyQt5
- Baseado no WhatsApp Web
- Interface otimizada para desktop
- Código aberto e documentado

## 🤝 Contribuição

1. Fork o projeto
2. Crie sua Feature Branch
3. Commit suas alterações
4. Push para a Branch
5. Abra um Pull Request

## 📞 Suporte

- Abra uma issue para reportar bugs
- Sugestões são bem-vindas
- Documentação disponível no código

## 🔄 Atualizações

- Verificar regularmente por atualizações
- Manter dependências atualizadas
- Acompanhar changelog

## 🌟 Recursos Futuros

- Backup de instâncias
- Notificações desktop
- Temas personalizados
- Atalhos de teclado
- Mais opções de personalização

## 📦 Caso queirar gerar um .exe Instalação
COMANDO : python -m PyInstaller --name="WhatsApp Multi-Instância" --onefile --noconsole --icon="whatsapp.ico" --add-binary="whatsapp.ico;." --hidden-import=PyQt5.QtWebEngineWidgets --hidden-import=PyQt5.QtWebEngineCore --hidden-import=PyQt5.QtWebEngine --hidden-import=PyQt5.QtNetwork --add-data="whatsapp.ico;." app.py
