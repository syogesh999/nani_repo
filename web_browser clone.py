import sys
from PyQt5.QtCore import QUrl
from PyQt5.QtGui import QIcon
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtWidgets import (QMainWindow, QApplication, QStatusBar, QToolBar,
                             QAction, QLineEdit, QTabWidget, QWidget, QVBoxLayout,
                             QPushButton)

class Tab(QWidget):
    def __init__(self, window, parent=None):
        super(Tab, self).__init__(parent)
        self.window = window
        layout = QVBoxLayout()
        self.browser = QWebEngineView()
        self.browser.setUrl(QUrl('https://www.bing.com'))
        self.browser.urlChanged.connect(self.update_AddressBar)
        layout.addWidget(self.browser)
        self.setLayout(layout)

    def update_AddressBar(self, url):
        self.window.URLBar.setText(url.toString())
        self.window.URLBar.setCursorPosition(0)

class Window(QMainWindow):
    def __init__(self, *args, **kwargs):
        super(Window, self).__init__(*args, **kwargs)
        
        self.tabs = QTabWidget()
        self.tabs.setTabsClosable(True)
        self.tabs.tabCloseRequested.connect(self.closeTab)
        self.tabs.addTab(Tab(self), "New Tab")
        self.setCentralWidget(self.tabs)

        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)

        self.navigation_bar = QToolBar('Navigation Toolbar')
        self.addToolBar(self.navigation_bar)

        back_button = QAction(QIcon('back_icon.png'), "Back", self)
        back_button.setStatusTip('Go to previous page you visited')
        back_button.triggered.connect(self.currentTab().browser.back)
        self.navigation_bar.addAction(back_button)

        refresh_button = QAction(QIcon('refresh_icon.png'), "Refresh", self)
        refresh_button.setStatusTip('Refresh this page')
        refresh_button.triggered.connect(self.currentTab().browser.reload)
        self.navigation_bar.addAction(refresh_button)

        next_button = QAction(QIcon('next_icon.png'), "Next", self)
        next_button.setStatusTip('Go to next page')
        next_button.triggered.connect(self.currentTab().browser.forward)
        self.navigation_bar.addAction(next_button)

        home_button = QAction(QIcon('home_icon.png'),"Home", self)
        home_button.setStatusTip('Go to home page (Bing)')
        home_button.triggered.connect(self.go_to_home)
        self.navigation_bar.addAction(home_button)

        google_button = QPushButton(QIcon('google_icon.png'), '', self)
        google_button.clicked.connect(lambda: self.updateSearchEngine("https://www.google.com/search?q="))
        self.navigation_bar.addWidget(google_button)

        bing_button = QPushButton(QIcon('bing_icon.png'), '', self)
        bing_button.clicked.connect(lambda: self.updateSearchEngine("https://www.bing.com/search?q="))
        self.navigation_bar.addWidget(bing_button)

        self.navigation_bar.addSeparator()

        self.URLBar = QLineEdit()
        self.URLBar.returnPressed.connect(self.loadURL)
        self.navigation_bar.addWidget(self.URLBar)

        self.addToolBarBreak()

        bookmarks_toolbar = QToolBar('Bookmarks', self)
        self.addToolBar(bookmarks_toolbar)

        pythongeeks = QAction("PythonGeeks", self)
        pythongeeks.setStatusTip("Go to PythonGeeks website")
        pythongeeks.triggered.connect(lambda: self.go_to_URL(QUrl("https://pythongeeks.org")))
        bookmarks_toolbar.addAction(pythongeeks)

        facebook = QAction(QIcon('facebook_icon.png'), "Facebook", self)
        facebook.setStatusTip("Go to Facebook")
        facebook.triggered.connect(lambda: self.go_to_URL(QUrl("https://www.facebook.com")))
        bookmarks_toolbar.addAction(facebook)

        linkedin = QAction(QIcon('linkedin_icon.png'),"LinkedIn", self)
        linkedin.setStatusTip("Go to LinkedIn")
        linkedin.triggered.connect(lambda: self.go_to_URL(QUrl("https://in.linkedin.com")))
        bookmarks_toolbar.addAction(linkedin)

        instagram = QAction(QIcon('instagram_icon.png'), "Instagram", self)
        instagram.setStatusTip("Go to Instagram")
        instagram.triggered.connect(lambda: self.go_to_URL(QUrl("https://www.instagram.com")))
        bookmarks_toolbar.addAction(instagram)

        twitter = QAction(QIcon('twitter_icon.png'), "Twitter", self)
        twitter.setStatusTip('Go to Twitter')
        twitter.triggered.connect(lambda: self.go_to_URL(QUrl("https://www.twitter.com")))
        bookmarks_toolbar.addAction(twitter)

        self.show()

    def currentTab(self):
        if self.tabs.count() > 0:
            return self.tabs.currentWidget()
        return None

    def closeTab(self, index):
        self.tabs.removeTab(index)

    def go_to_home(self):
        if self.currentTab():
            self.currentTab().browser.setUrl(QUrl('https://www.bing.com/'))

    def loadURL(self):
        if self.currentTab():
            url = QUrl(self.URLBar.text())
            if url.scheme() == '':
                url.setScheme('https://')
            self.currentTab().browser.setUrl(url)
            self.currentTab().update_AddressBar(url)

    def go_to_URL(self, url: QUrl):
        if self.currentTab():
            self.currentTab().browser.setUrl(url)
            self.currentTab().update_AddressBar(url)

    def updateSearchEngine(self, search_engine):
        self.search_engine = search_engine

        # Update the URLBar text to reflect the selected search engine
        if self.currentTab():
            current_url = self.currentTab().browser.url()
            if current_url:
                current_query = current_url.query()
                self.URLBar.setText(f"{self.search_engine}{current_query}")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setApplicationName('Professional Web Browser')

    window = Window()
    app.exec_()
