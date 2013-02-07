from bs4 import BeautifulSoup
import os
import re 
import cgi

root_dir = 'otp_doc_html_R16A_RELEASE_CANDIDATE/'
#app_list
#app_list = os.listdir('otp_doc_html_R16A_RELEASE_CANDIDATE/lib')
#app_list = [x.split('-')[0] for x in app_list]

app_html = open('otp_doc_html_R16A_RELEASE_CANDIDATE/doc/applications.html','r')
app_soup = BeautifulSoup(app_html).find_all('tr')
app_category = ''
app_list = []
sql_app_id_iter = 0
sql_app_id_lookup = {}
app_link_lookup = {}
for i in range(0, len(app_soup)):
    if len(app_soup[i].attrs) == 0:
        if len(app_soup[i].td.attrs) == 2:
            app_category = app_soup[i].td.font.b.text.strip().encode('UTF-8') # App Category
   #         print app_soup[i].td.font.b.text # App Category
    elif len(app_soup[i].attrs) == 1:
        td_list = app_soup[i].find_all('td')
        if len(td_list) == 3:
           #print app_cat
           a_list = td_list[1].find_all('a')
           #print a_list[0].text # App Name
           #print a_list[1].text # App Version
           #print td_list[2].text.strip() # App Summary
           app_link = root_dir + a_list[0]['href'].strip().encode('UTF-8')[3:] # App URL 
           app_name = a_list[0].text.strip().encode('UTF-8') # App Name
           app_version = a_list[1].text.strip().encode('UTF-8') # App Version
           app_summary = td_list[2].text.strip().encode('UTF-8') # App Summary
           app_summary = [x.encode('UTF-8') for x in app_summary if x != '\n' ]
           app_summary = ''.join(map(str, app_summary))
           app_summary = re.sub(' +',' ', app_summary)
	   app_list.append((app_name,app_version,app_summary,app_category))
	   sql_app_id_iter += 1 
	   sql_app_id_lookup[app_name] = sql_app_id_iter
	   app_link_lookup[app_name] = app_link 
        #if td_list[0].table != None:
            #print app_soup[i].td.table.tr.td.find_all('a')
            #a_list = app_soup[i].td.table.tr.td.find_all('a')
            #print a_list[0].text # App Name
            #print a_list[1].text # App Version
    #if i > 1:
    #    break;

sql_apps = ''
for i in range(0, len(app_list)):
    sql_apps += "INSERT INTO apps (name,version,summary) "
    sql_apps += 'VALUES ("'+app_list[i][0]+'","'+app_list[i][1]+'","'+app_list[i][2]+'");' 
    sql_apps += "\n"
    sql_apps += "\n"

f = open('sql_apps.sql', 'w')
f.write(sql_apps)
f.close()

#print app_list[0]
#('erts', '5.10', 'Functionality necessary to run the Erlang System itself', 'Basic')
#name version summary category
#INSERT INTO table_name (name,version,summary,category)
#VALUES (value1, value2, value3,...)
#print len(app_list) # 54
#print sql_app_id_lookup
#print sql_app_id_lookup['Basic'] # 1
#print sql_app_id_lookup['Miscellaneous'] # 9
#print len(sql_app_id_lookup) # 54 
#print app_link_lookup
#print len(app_link_lookup) # 54

"""
Going Through Each App and Scraping.
"""
"""
dir = app_link_lookup["sasl"]
app_html = open(dir,'r')
app_soup = BeautifulSoup(app_html).find('ul', {'class':'flipMenu'})
print app_soup.prettify()
"""

"""
craping stdlib
"""
app_id = sql_app_id_lookup['stdlib'] # 5
dir = app_link_lookup["stdlib"]
app_html = open(dir,'r')
flip_soup = BeautifulSoup(app_html).find('ul', {'class':'flipMenu'})



#####
#app html
#####
first_li = flip_soup.find('li')
#print first_li.a.text.encode('UTF-8').strip()
href = first_li.a["href"]
app_href = dir[:-10] + href 
#print app_href
app_info_page = open(app_href,'r')
app_info_soup = BeautifulSoup(app_info_page).find('div', {'id':'content'}).div
#print app_info_soup
info = app_info_soup.find_all('div',{"class":"REFBODY"})
module = info[0].text.strip()
summary = info[1].text.strip()
#print info[2].findAll("p")[1].text
#description = info[2].p.p.text
description = info[2].findAll("p")[1].text
description = [x.encode('UTF-8') for x in description if x != '\n' ]
description = [x for x in description if x != '' ]
description = ''.join(map(str, description))
description = re.sub(' +',' ',description)
configuration = info[3]
see_also = info[4].p.text
see_also = [x.encode('UTF-8') for x in see_also if x != '\n' ]
see_also = ''.join(map(str, see_also))
see_also = re.sub(' +',' ', see_also)
#print module
#print summary
#print description
#print see_also

"""
Going through the table of contents lists with folders icon
"""
def soupify(url):
    html_file = open(url,'r')
    return BeautifulSoup(html_file)

li_list = flip_soup.findAll('li',{'id':'no'})
for i in range(0, len(li_list)):
    if i > 2:
        break
    href = li_list[i].a["href"]
    href = dir[:-10] + href 
    soup = soupify(href)
    soup = soup.find("div",{"id":'content'}).find("div",{"class":"innertube"})
    info = soup.find_all('div',{"class":"REFBODY"})
    module = info[0].text.strip()
    summary = info[1].text.strip()
    description = info[2].p

#print module
#print summary
#print description
#print soup.contents[18]
#print soup.contents[34].name
#function = soup.contents[34].find('a')['name']
#print function 
FLAG_FUNCTION_SECTION = False
for i in range(0, len(soup.contents)):
    FLAG_FUNCTION_SEE_MORE = False
    #if i > 36:
    #if i > 42:
    #    break
    if (
            FLAG_FUNCTION_SECTION and
            hasattr(soup.contents[i], 'name') and 
            soup.contents[i].name == 'p' 
       ):
        #print soup.contents[i]
        fun_list = soup.contents[i].findAll("a",{"name":True})
	fun_list_name = []
	#print len(fun_list)
	for j in range(0, len(fun_list)):
	    fun_list_name.append(str(fun_list[j]["name"]))
	#print fun_list_name
	#print fun_list 
        syntax_list = soup.contents[i].findAll("span",{"class":"bold_code"})
	syntax_list = [x.renderContents() for x in syntax_list]
	fun_name_syntax_list = zip(fun_list_name, syntax_list)
	#print fun_name_syntax_list
        #function_syntax = soup.contents[i].span.text
        #function_syntax = cgi.escape(function_syntax).encode("ascii", "xmlcharrefreplace")
	#print i
        #print function_syntax
        """
        fun_info = soup.contents[i+1].p.text
        fun_info = soup.contents[i+1].p.text
        #print fun_info
        #print 'end'
        """
        types = ''
        if (
                hasattr(soup.contents[i+1], 'p') and
                soup.contents[i+1].p.text == "Types:"
           ):
            types = soup.contents[i+1].div
            types = [x.encode('UTF-8') for x in types if x != '\n' ]
            types = [x for x in types if x != '' ]
            types = ''.join(map(str, types))
            types = re.sub(' +',' ',types)
            types = re.sub('\n',' ',types)
            #print types
            fun_info = soup.contents[i+3].findAll("p")
        else:
            fun_info = soup.contents[i+2].findAll("p")
        #function_name = fun_info[0].a["name"]
        #function_name = cgi.escape(function_name).encode("ascii", "xmlcharrefreplace")
        #print function_name
        if len(fun_info) == 3 and hasattr(fun_info[2], 'strong'):
	    if hasattr(fun_info[2].strong, 'content'):
	        if fun_info[2].strong.contents == "See also:":
            	    see_more = fun_info[2].span.a.text.strip()
		    FLAG_FUNCTION_SEE_MORE = True 
	function_summary = ''
        if FLAG_FUNCTION_SEE_MORE: 
            function_summary = fun_info[1].contents
            function_summary = [x.encode('UTF-8') for x in function_summary if x != '\n' ]
            function_summary = [x for x in function_summary if x != '' ]
            function_summary = ''.join(map(str, function_summary))
            function_summary = re.sub(' +',' ',function_summary)
            function_summary = re.sub('\n',' ',function_summary)
	else:
	    for l in range(1,len(fun_info)):
	        function_summary_temp = fun_info[l].contents
                function_summary_temp = ''.join(map(str, function_summary_temp))
                function_summary += str(function_summary_temp)
                function_summary = [x.encode('UTF-8') for x in function_summary if x != '\n' ]
                function_summary = [x for x in function_summary if x != '' ]
                function_summary = ''.join(map(str, function_summary))
                function_summary = re.sub(' +',' ',function_summary)
                function_summary = re.sub('\n',' ',function_summary)
		print function_summary
        #print function_summary[0]
	#print fun_name_syntax_list
	for k in range(0,len(fun_name_syntax_list)):
	    fun_name_syntax_list[k] = tuple(list(fun_name_syntax_list[k]) + [function_summary])
	#print fun_name_syntax_list[k]

    if (
            hasattr(soup.contents[i], 'name') and 
            soup.contents[i].name == 'h3' and
            soup.contents[i].text.strip() == 'EXPORTS' 
       ):
        FLAG_FUNCTION_SECTION = True
            



"""
		if i > 0:
			print i
			#print soup.contents[i].prettify()
			function = soup.contents[i].find('a')['name']
			print "function:"
			print function
			semantic = soup.contents[i].find('span').text.strip()
			#print "semantic:"
			#print semantic
			types = soup.contents[i].div.contents
			types = soup.contents[i].div.p.replaceWith('')
			types = soup.contents[i].div.contents
			types = [x.encode('UTF-8') for x in types if x != '\n' ]
			types = [x for x in types if x != '' ]
			types = ''.join(map(str, types))
			types = BeautifulSoup(types).prettify()
			print "types:"
			print types
			summary = soup.contents[i+2].findChildren()[0].findChildren()[0]
			print "summary:"
			print summary

"""


"""
#print app_soup[1]
#for i in range(0, len(app_soup)):
#    print app_soup[i]
#    if i > 2:
#        break;

lists = open("lib/stdlib-1.19/doc/html/lists.html", "r")
soup = BeautifulSoup(lists)
#soup = BeautifulSoup(soup.prettify().encode('UTF-8'))

#print soup.prettify().encode('UTF-8')

soup = soup.find("div",{"id":'content'}).find("div",{"class":"innertube"})


#soup = BeautifulSoup(soup.prettify().encode('UTF-8'))


info = soup.find_all('div',{"class":"REFBODY"})
module = info[0].text.strip()
summary = info[1].text.strip()
description = info[2]
description = BeautifulSoup(description.prettify()).html.body.div.contents
description = [x.encode('UTF-8') for x in description if x != '\n' ]
description = [x for x in description if x != '' ]
description = ''.join(map(str, description))
#print description

#print len(soup.contents)
#print soup.contents[4].name
for i in range(0, len(soup.contents)):
	if hasattr(soup.contents[i], 'name') and soup.contents[i].name == 'p':
		if i > 24:
			print i
			#print soup.contents[i].prettify()
			function = soup.contents[i].find('a')['name']
			print "function:"
			print function
			semantic = soup.contents[i].find('span').text.strip()
			#print "semantic:"
			#print semantic
			types = soup.contents[i].div.contents
			types = soup.contents[i].div.p.replaceWith('')
			types = soup.contents[i].div.contents
			types = [x.encode('UTF-8') for x in types if x != '\n' ]
			types = [x for x in types if x != '' ]
			types = ''.join(map(str, types))
			types = BeautifulSoup(types).prettify()
			print "types:"
			print types
			summary = soup.contents[i+2].findChildren()[0].findChildren()[0]
			print "summary:"
			print summary

	if i > 26:
		break
#i = 0
#for content in soup.contents:
	#print i
#	i += 1
#	if content != '':
#		print ''
		#print soup.contents[i]
#		print soup.contents[i].name
#	if i > 3:
#		break
#print(soup.contents[0])
#print(soup.contents[3])
#tag name
#print soup.contents[4].name
"""
