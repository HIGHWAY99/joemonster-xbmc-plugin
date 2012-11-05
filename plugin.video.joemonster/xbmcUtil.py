# Utility functions for xbmc

import sys,urllib, xbmcplugin,xbmcgui, xbmc


class ViewAddonAbstract:
	viewMap = {}

	def addHandler(self, name, handler):
		if (len(self.viewMap)==0):
			self.viewMap[None] = handler
		self.viewMap[name] = handler

	def setVideoHandler(self, handler):
		videoHandler = handler
   
	def handle(self):
		params = getParams()
		view = getParam(params, "view")
		pg = getParam(params, "pg")
		if (pg ==None):
			pg = 1

		if (view == 'video'):
			link = getParam(params, "link")
			self.playVideo(link)
			return

		try:	
			hdlFunc = self.viewMap[view]
		except:
			notification('Error', 'Could not open view: ' + view)
		
		hdlFunc(int(pg), params)
		endOfDir()

	def playVideo(self, link):
		resolvedVideoLink =	self.handleVideo(link)
		if (resolvedVideoLink!=None):
			liz=xbmcgui.ListItem(path=resolvedVideoLink)
			xbmcplugin.setResolvedUrl(0, True, liz)
		else:
			print ("could not play " + link)
			xbmcUtil.notification(header="Warning", message="Could not play video, youtube and joemonster videos are supported")
		

	def handleVideo(link):
		print('abstract')

	def addViewLink(self, title, view, pg=1, params={}):
		u=sys.argv[0] + "?view=" + str(view) + "&pg=" + str(pg)
		for key in params.iterkeys():
			u = u + "&" + key + "=" + urllib.quote_plus(params[key])
		print(u)	
		icon = "DefaultVideoPlaylists.png"
	
		liz=xbmcgui.ListItem(title, iconImage=icon, thumbnailImage='')
		liz.setProperty("IsPlayable", "false")
		liz.setInfo( type="Video", infoLabels={ "Title": title } )
		xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]), url=u,listitem=liz, isFolder=True)

	def addVideoLink(self, title, link, img, plot=''):
		u=sys.argv[0] + "?view=video&link=" +  urllib.quote_plus(link) + "&name=" + title
		icon= "DefaultVideo.png"
		liz=xbmcgui.ListItem(title, iconImage=icon, thumbnailImage=img)
		liz.setProperty("IsPlayable", "true")
		liz.setInfo( type="Video", infoLabels={ "Title": title, 'plot': plot } )
		xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]), url=u,listitem=liz, isFolder=False)

	def addDirectVideoLink(self, name, link, img):
		u=link
		icon= "DefaultVideo.png"
		liz=xbmcgui.ListItem(name, iconImage=icon, thumbnailImage=img)
		liz.setProperty("IsPlayable", "true")
		liz.setInfo( type="Video", infoLabels={ "Title": name } )
		xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]), url=u,listitem=liz, isFolder=False)



def addDir(name, page, autoplay, isPlayable = True):
	u=sys.argv[0] + "?page=" + str(page)
	icon = "DefaultVideoPlaylists.png"
	if autoplay:
	  icon= "DefaultVideo.png"
	liz=xbmcgui.ListItem(name, iconImage=icon, thumbnailImage='')
	if autoplay and isPlayable:
	  liz.setProperty("IsPlayable", "true")
	liz.setInfo( type="Video", infoLabels={ "Title": name } )
	xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]), url=u,listitem=liz, isFolder= not autoplay)


def endOfDir():
	xbmcplugin.endOfDirectory(int(sys.argv[1]))







def addDirLink(name, page, link, autoplay, isPlayable = True):
	u=sys.argv[0] + "?page=" + str(page) + "&link=" +  urllib.quote_plus(link) + "&name=" + name
	icon = "DefaultVideoPlaylists.png"
	if autoplay:
	  icon= "DefaultVideo.png"
	liz=xbmcgui.ListItem(name, iconImage=icon, thumbnailImage='')
	if autoplay and isPlayable:
	  liz.setProperty("IsPlayable", "true")
	liz.setInfo( type="Video", infoLabels={ "Title": name } )
	xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]), url=u,listitem=liz, isFolder= not autoplay)



def addLink(name,url,iconimage):
	    ok=True
	    liz=xbmcgui.ListItem(name, iconImage="DefaultVideo.png", thumbnailImage=iconimage)
	    liz.setInfo( type="Video", infoLabels={ "Title": name } )
	    print(sys.argv[1])

	    print(sys.argv)
	    ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=url,listitem=liz)
	    return ok


def getParams():    
	param={}
	paramstring=sys.argv[2]
	#self.log.debug('raw param string: ' + paramstring)
	if len(paramstring)>=2:
	  params=sys.argv[2]
	  cleanedparams=params.replace('?','')
	  if (params[len(params)-1]=='/'):
	    params=params[0:len(params)-2]
	  pairsofparams=cleanedparams.split('&')
	  param={}
	  for i in range(len(pairsofparams)):
	    splitparams={}
	    splitparams=pairsofparams[i].split('=')
	    if (len(splitparams))==2:
	      param[splitparams[0]]=urllib.unquote_plus(splitparams[1])
	return param


def getParam(params, name):
	try:
	  result = params[name]
	  result = result
	  #result = urllib.unquote_plus(result)
	  return result
	except:
	  return None


def notification(header="", message="", sleep=5000 ):
	""" Will display a notification dialog with the specified header and message,
	    in addition you can set the length of time it displays in milliseconds and a icon image. 
	"""
	xbmc.executebuiltin( "XBMC.Notification(%s,%s,%i)" % ( header, message, sleep ) )



