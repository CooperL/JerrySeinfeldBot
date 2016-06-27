from bs4 import BeautifulSoup
from urllib.request import urlopen
import os

BASE_URL = "http://www.seinfeldscripts.com/"

def get_ep_links(SectionUrl):
	html = urlopen(SectionUrl).read()
	soup = BeautifulSoup(html, "lxml")
	EpTable = soup.find("table", width="670")
	#print(EpTable.prettify())
	EpTags = EpTable.findAll(href=True)
	EpLinks = []
	for item in EpTags:
		link = item["href"]
		if link[0].isspace():
			EpTitle = link.lstrip()
		else:
			EpTitle = link
		EpLinks.append(EpTitle)
	return EpLinks

def get_script_html(LinkList):
	for ep in LinkList:
		ep_html = urlopen(BASE_URL + ep).read()
		soup = BeautifulSoup(ep_html, "lxml")
		ScriptContent = soup.findAll("div", id="content")
		ScriptTags = ScriptContent[0].findAll("p")
		ScriptTextList = []
		# print(ScriptTags)
		for item in ScriptTags:
			ScriptTextList.append(item.renderContents())
		for item in ScriptTextList:
			tempStr = str(item)
			item = tempStr[2:-1]
		ScriptText = ScriptTextList[0:len(ScriptTextList)]
		print(ScriptText)
		path = "RawHTML_Scripts/"
		if not os.path.exists(path):
			os.makedirs(path)
		file_name = path + str(ep[:-5]) + ".txt"
		ScriptFile = open(file_name, "w+")
		ScriptFile.write(str(ScriptText))
		ScriptFile.close()

def clean_script_text(ScriptPath):
	files = os.listdir(ScriptPath)
	OutPath = "Scripts/"
	if not os.path.exists(OutPath):
		os.makedirs(OutPath)
	for ep in files:
		if ep[:1] != '.':
			file_name = ep
			print(ep)
			ScriptFile = open(ScriptPath + file_name, "r")
			# print(ScriptFile)
			SepScript = ScriptFile.read().split()
			CleanedSepScript = []
			for item in SepScript:
				if item[:1] not in ['/', '<', '>', '[', ']', '\\', '\'', '(', ')', '-', '"']:
					CleanedSepScript.append(item)
			# print(CleanedSepScript)

def main():
	links = get_ep_links(BASE_URL + "seinfeld-scripts.html")
	get_script_html(links)
	# clean_script_text("RawHTML_Scripts/")