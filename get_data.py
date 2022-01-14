import urllib, urllib2, cookielib, sys, time, re, copy, os, traceback

# Global variables
user_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'
# header variable
headers = { 'User-Agent' : user_agent }

cj = cookielib.CookieJar()
opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))

output_filename = 'nmr.tsv'
if os.path.exists(output_filename):
    fout = open(output_filename, 'a')
else:
    fout = open(output_filename, 'w')

def get_cnmr(str_in, formula):
    lines = str_in.strip().split('\n')
    lines_out = []
    for line in lines:
        items = line.strip().split()
        if len(items) < 3:
            continue
        if len(items) == 3:
            if is_float(items[0]) and is_float(items[1]):
                lines_out.extend(items)
                continue
            else:
                continue
        # replace *
        line_out = re.sub(r'\*[^\s]*', ' ', line)
        items = line_out.strip().split()
        if len(items) < 3:
            continue
        if len(items) == 3:
            if is_float(items[0]) and is_float(items[1]):
                lines_out.extend(items)
                continue
            else:
                continue
        # for P and F
        if 'P' in formula:
            line_out = re.sub(r'\s+P\s+', ' ', line_out, 1)
            items = line_out.strip().split()
            if len(items) < 3:
                continue
            if len(items) == 3:
                if is_float(items[0]) and is_float(items[1]):
                    lines_out.extend(items)
                    continue
                else:
                    continue
            line_out = re.sub(r'\s+P[^\s]*', ' ', line_out, 1)
            items = line_out.strip().split()
            if len(items) < 3:
                continue
            if len(items) == 3:
                if is_float(items[0]) and is_float(items[1]):
                    lines_out.extend(items)
                    continue
                else:
                    continue
        if 'F' in formula:
            line_out = re.sub(r'\s+F\s+', ' ', line_out, 1)
            items = line_out.strip().split()
            if len(items) < 3:
                continue
            if len(items) == 3:
                if is_float(items[0]) and is_float(items[1]):
                    lines_out.extend(items)
                    continue
                else:
                    continue
            line_out = re.sub(r'\s+F[^\s]*', ' ', line_out, 1)
            items = line_out.strip().split()
            if len(items) < 3:
                continue
            if len(items) == 3:
                if is_float(items[0]) and is_float(items[1]):
                    lines_out.extend(items)
                    continue
                else:
                    continue
        # comments
        line_out = re.sub(r'\s+\d+\)', ' ', line_out)
        items = line_out.strip().split()
        if len(items) < 3:
            continue
        if len(items) == 3:
            if is_float(items[0]) and is_float(items[1]):
                lines_out.extend(items)
                continue
            else:
                continue
    return lines_out

def get_hnmr(str_in, formula):
    lines = str_in.strip().split('\n')
    lines_out = []
    for line in lines:
        # remove J(A,B)
        m = re.search(r'\s+J\([^\s]*?,[^\s]*?\)', line)
        if m:
            continue
        items = line.strip().split()
        if len(items) < 2:
            continue
        if len(items) == 2:
            if is_float(items[1]):
                lines_out.extend(items)
                continue
            else:
                continue
        # replace *
        line_out = re.sub(r'\*[^\s]*', ' ', line)
        items = line_out.strip().split()
        if len(items) < 2:
            continue
        if len(items) == 2:
            if is_float(items[1]):
                lines_out.extend(items)
                continue
            else:
                continue
        # comments
        line_out = re.sub(r'\s+\d+\)', ' ', line_out)
        items = line_out.strip().split()
        if len(items) < 2:
            continue
        if len(items) == 2:
            if is_float(items[1]):
                lines_out.extend(items)
                continue
            else:
                continue
    return lines_out

def get_hnmr_details(str_in, formula):
    lines = str_in.strip().split('\n')
    lines_out = []
    for line in lines:
        items = line.strip().split()
        if len(items) < 3:
            continue
        if len(items) == 3:
            if is_float(items[0]) and is_float(items[1]) and is_float(items[2]):
                lines_out.extend(items)
                continue
            else:
                continue
        # replace *
        line_out = re.sub(r'\*[^\s]*', ' ', line)
        items = line_out.strip().split()
        if len(items) < 3:
            continue
        if len(items) == 3:
            if is_float(items[0]) and is_float(items[1]) and is_float(items[2]):
                lines_out.extend(items)
                continue
            else:
                continue
        # comments
        line_out = re.sub(r'\s+\d+\)', ' ', line_out)
        items = line_out.strip().split()
        if len(items) < 3:
            continue
        if len(items) == 3:
            if is_float(items[0]) and is_float(items[1]) and is_float(items[2]):
                lines_out.extend(items)
                continue
            else:
                continue
    return lines_out

def is_float(f):
    try:
        a = float(f)
        return True
    except Exception as e:
        return False

# If there is a disclaimer or not
def is_disclaimer(html):
    p_disclaimer = '<FRAME.*?src="/sdbs/cgi-bin/cre_disclaimer.cgi'
    m = re.search(p_disclaimer, html)
    if m:
        return True
    else:
        return False


def click_disclaimer_init():
    # top part frame
    url = 'https://sdbs.db.aist.go.jp/sdbs/cgi-bin/direct_frame_top.cgi'
    request = urllib2.Request(url, None, headers)
    response = opener.open(request)
    # bottom part frame
    url = 'https://sdbs.db.aist.go.jp/sdbs/cgi-bin/cre_disclaimer.cgi?REQURL=/sdbs/cgi-bin/cre_search.cgi&amp;amp;REFURL='
    request = urllib2.Request(url, None, headers)
    response = opener.open(request)
    # click disclaimer
    url = 'https://sdbs.db.aist.go.jp/sdbs/cgi-bin/ENTRANCE.cgi'
    request = urllib2.Request(url, urllib.urlencode({'lang':'eng', 'REQURL':'/sdbs/cgi-bin/cre_search.cgi', 'REFURL':''}), headers)
    response = opener.open(request)

def click_disclaimer(response):
    m = re.search(r'src="(/sdbs/cgi-bin/cre_disclaimer.cgi.*?)"', response)
    assert m, 'ERROR:\n'+response
    ur = 'https://sdbs.db.aist.go.jp' + m.group(1)
    # top part frame
    url = 'https://sdbs.db.aist.go.jp/sdbs/cgi-bin/cre_list.cgi'
    request = urllib2.Request(url, None, headers)
    response = opener.open(request)
    # bottom part frame
    request = urllib2.Request(ur, None, headers)
    response = opener.open(request).read()
    # click disclaimer
    url = 'https://sdbs.db.aist.go.jp/sdbs/cgi-bin/ENTRANCE.cgi'
    lang = re.search(r'name="lang"\s*value="(.*?)"', response).group(1)
    REQURL = re.search(r'name="REQURL"\s*value="(.*?)"', response).group(1)
    REFURL = re.search(r'name="REFURL"\s*value="(.*?)"', response).group(1)
    request = urllib2.Request(url, urllib.urlencode({'lang':lang, 'REQURL':REQURL, 'REFURL':REFURL}), headers)
    response = opener.open(request).read()
    url = 'https://sdbs.db.aist.go.jp/sdbs/cgi-bin/cre_list.cgi'
    request = urllib2.Request(url, None, headers)
    response = opener.open(request).read()
    url = 'https://sdbs.db.aist.go.jp/sdbs/cgi-bin/cre_search.cgi'
    request = urllib2.Request(url, None, headers)
    response = opener.open(request).read()
    return response

def open_search():
    # Open Search Page
    url = 'https://sdbs.db.aist.go.jp/sdbs/cgi-bin/cre_search.cgi'
    request = urllib2.Request(url, None, headers)
    response = opener.open(request)
    m = is_disclaimer(response.read())
    if m:
        click_disclaimer_init()
    request = urllib2.Request(url, None, headers)
    response = opener.open(request)
    html = response.read()
    m = is_disclaimer(html)
    assert not m, 'ERROR, click disclaimer invalid'+sys.exit(1)

    return html

def search(html, mw_from, mw_to, cur_page):
    m = re.search('<form.*?action="(.*?)".*?POST', html)
    assert m, 'ERROR: parse search page failed'
    action = m.group(1)
    data = [
        ('compname', ''),
        ('match_type', '1'),
        ('formula', ''),
        ('mw_from', str(mw_from)),
        ('mw_to', str(mw_to)),
        ('regno', ''),
        ('sdbsno', ''),
        ('c_from', ''),
        ('c_to', ''),
        ('h_from', ''),
        ('h_to', ''),
        ('n_from', ''),
        ('n_to', ''),
        ('o_from', ''),
        ('o_to', ''),
        ('f_from', ''),
        ('f_to', ''),
        ('cl_from', ''),
        ('cl_to', ''),
        ('br_from', ''),
        ('br_to', ''),
        ('i_from', ''),
        ('i_to', ''),
        ('s_from', ''),
        ('s_to', ''),
        ('p_from', ''),
        ('p_to', ''),
        ('si_from', ''),
        ('si_to', ''),
        ('spectrum', '3'),
        ('spectrum', '5'),
        ('ir_value_st', ''),
        ('ir_range', '10'),
        ('ir_trans_st', '80'),
        ('cnmr_value_st', ''),
        ('cnmr_range', '2.0'),
        ('cnmr_not_st', ''),
        ('hnmr_value_st', ''),
        ('hnmr_range', '2.0'),
        ('hnmr_not_st', ''),
        ('massno_st', ''),
        ('submit', 'Search'),
        ('page_list', '100'),
        ('order_opt', '1'),
        ('order_desc', '0'),
    ]
    data_send = copy.deepcopy(data)
    data_send.append(('cur_page', str(cur_page)))
    url = 'https://sdbs.db.aist.go.jp/sdbs/cgi-bin/'+action
    request = urllib2.Request(url, urllib.urlencode(data_send), headers)
    response = opener.open(request).read()
    m = is_disclaimer(response)
    if m:
        response = click_disclaimer(response)
        m = re.search('<form.*?action="(.*?)".*?POST', html)
        assert m, 'ERROR: parse search page failed'+response
        action = m.group(1)
        url = 'https://sdbs.db.aist.go.jp/sdbs/cgi-bin/'+action
        request = urllib2.Request(url, urllib.urlencode(data_send), headers)
        response = opener.open(request).read()
        m = is_disclaimer(response)
    assert not m, 'ERROR:\n'+response+sys.exit(1)
    return response

def read_molecules(search_html):
    p = re.compile(r'\<tr\>(.*?)\</tr\>', re.MULTILINE | re.DOTALL)
    matches = re.finditer(p, search_html)
    for m in matches:
        try:
            print ('------')
            start = m.start(1)
            end = m.end(1)
            l = search_html[start:end]
            m2 = re.search(r'onClick="return\s*clickLoggingDict\(\'(.*?)\',\s*\'(.*?)\'\)', l)
            if not m2:
                assert False, 'ERROR: parse search result failed'
                continue
            sdbsno = m2.group(1)
            compname = m2.group(2)
            print (sdbsno)
            print (compname)
            p_td = re.compile(r'\<td.*?\>(.*?)\</td\>', re.MULTILINE | re.DOTALL)
            matches2 = re.finditer(p_td, l)
            formula = ''
            cas = ''
            mw = -1
            for idx, m3 in enumerate(matches2):
                if idx == 3:
                    formula = m3.group(1)
                    print (formula)
                if idx == 4:
                    mw = float(m3.group(1))
                    print (mw)
                if idx == 7:
                    m4 = re.search(r'([-\d]+)', m3.group(1))
                    if not m4:
                        continue
                    cas = m4.group(1)
                    print (cas)
            if formula == '' or mw < 0 or cas == '':
                assert False, 'ERROR: invalid formula or mw or cas'
                continue
            # sdbsno, compname, formula, mw, cas
            # get CNMR
            url = 'https://sdbs.db.aist.go.jp/sdbs/cgi-bin/cre_frame_disp.cgi?spectrum_type=cnmr&amp;amp;sdbsno=%s'%sdbsno
            request = urllib2.Request(url, None, headers)
            response = opener.open(request).read()
            m_disclaimer = is_disclaimer(response)
            if m_disclaimer:
                click_disclaimer(response)
                request = urllib2.Request(url, None, headers)
                response = opener.open(request).read()
                m_disclaimer = is_disclaimer(response)
                assert not m_disclaimer, 'ERROR: click disclaimer failed'+response+sys.exit(1)
            m5 = re.search('<frame\s*SRC="\./(.*?img_disp\.cgi.*?)"', response)
            assert m5, 'ERROR: search fram failed\n'+response
            url = 'https://sdbs.db.aist.go.jp/sdbs/cgi-bin/' + m5.group(1)
            request = urllib2.Request(url, None, headers)
            response = opener.open(request).read()
            m_disclaimer = is_disclaimer(response)
            if m_disclaimer:
                click_disclaimer(response)
                request = urllib2.Request(url, None, headers)
                response = opener.open(request).read()
                m_disclaimer = is_disclaimer(response)
                assert not m_disclaimer, 'ERROR: click disclaimer failed'+response+sys.exit(1)
            p_pre = re.compile(r'\<pre.*?\>(.*?)\</pre\>', re.MULTILINE | re.DOTALL)
            matches3 = re.finditer(p_pre, response)
            cnmr = []
            cnmr_pre = ''
            for m6 in matches3:
                l = m6.group(1)
                m7 = re.search(r'ppm\s*Int.\s*Assign', l)
                if m7:
                    m8 = re.search(re.compile(r'([^\s].*)', re.DOTALL), re.sub(r'\<b\>.*?ppm\s*Int.*?\</b\>', '', l).replace('<br>', ''))
                    assert m8, 'ERROR: parse Int Assign failed'
                    cnmr_pre = m8.group(1).replace('\n','<_newline_>').replace('\t', ' ').strip()
                    cnmr_all = get_cnmr(m8.group(1).strip(), formula)
                    len_cnmr = len(cnmr_all)
                    num_groups = len_cnmr / 3
                    for i in range(num_groups):
                        if is_float(cnmr_all[i*3]) and is_float(cnmr_all[i*3+1]):
                            cnmr.append((float(cnmr_all[i*3]), float(cnmr_all[i*3+1]), cnmr_all[i*3+2]))
            print (cnmr)
            print (cnmr_pre)
            if len(cnmr) == 0:
                assert False, 'ERROR: cnmr length 0'
                continue
            # get HNMR
            url = 'https://sdbs.db.aist.go.jp/sdbs/cgi-bin/cre_frame_disp.cgi?spectrum_type=hnmr&amp;amp;sdbsno=%s'%sdbsno
            request = urllib2.Request(url, None, headers)
            response = opener.open(request).read()
            m_disclaimer = is_disclaimer(response)
            if m_disclaimer:
                click_disclaimer(response)
                request = urllib2.Request(url, None, headers)
                response = opener.open(request).read()
                m_disclaimer = is_disclaimer(response)
                assert not m_disclaimer, 'ERROR: click disclaimer invalid'+response+sys.exit(1)
            m5 = re.search('<frame\s*SRC="\./(.*?img_disp\.cgi.*?)"', response)
            assert m5, 'ERROR: parse img_disp failed'
            url = 'https://sdbs.db.aist.go.jp/sdbs/cgi-bin/' + m5.group(1)
            request = urllib2.Request(url, None, headers)
            response = opener.open(request).read()
            m_disclaimer = is_disclaimer(response)
            if m_disclaimer:
                click_disclaimer(response)
                response = opener.open(request).read()
                m_disclaimer = is_disclaimer(response)
                assert not m_disclaimer, 'ERROR: click disclaimer invalid'+response+sys.exit(1)
            p_pre = re.compile(r'\<pre.*?\>(.*?)\</pre\>', re.MULTILINE | re.DOTALL)
            matches4 = re.finditer(p_pre, response)
            hnmr = []
            hnmr_pre = ''
            for m6 in matches4:
                l = m6.group(1)
                m9 = re.search(r'Assign\.\s*Shift\(ppm\)', l)
                if m9:
                    m10 = re.search(re.compile(r'([^\s].*)', re.DOTALL), re.sub(r'\<b\>.*?Assign\.\s*Shift\(ppm\).*?\</b\>', '', l).replace('<br>', ''))
                    assert m10, 'ERROR: parse Assign Shift failed'
                    hnmr_pre = m10.group(1).replace('\n','<_newline_>').replace('\t', ' ').strip()
                    hnmr_all = get_hnmr(m10.group(1).strip(), formula)
                    len_hnmr = len(hnmr_all)
                    num_groups = len_hnmr / 2
                    for i in range(num_groups):
                        if is_float(hnmr_all[i*2+1]):
                            hnmr.append((hnmr_all[i*2], float(hnmr_all[i*2+1])))
            if len(hnmr) == 0:
                matches4 = re.finditer(p_pre, response)
                for m6 in matches4:
                    l = m6.group(1)
                    m9 = re.search(r'Parameter\s*ppm\s*Hz', l)
                    if m9:
                        m10 = re.search(re.compile(r'([^\s].*)', re.DOTALL), re.sub(r'\<b\>.*?Parameter\s*ppm.*?\</b\>', '', l).replace('<br>', ''))
                        assert m10, 'Parse Parameter ppm failed'
                        hnmr_pre = m10.group(1).replace('\n','<_newline_>').replace('\t', ' ').strip()
                        hnmr_all = get_hnmr(m10.group(1).strip(), formula)
                        len_hnmr = len(hnmr_all)
                        num_groups = len_hnmr / 2
                        for i in range(num_groups):
                            if is_float(hnmr_all[i*2+1]):
                                hnmr.append((hnmr_all[i*2], float(hnmr_all[i*2+1])))
            print (hnmr)
            print (hnmr_pre)
            if len(hnmr) == 0:
                assert False, 'ERROR: empty hmnr'
                continue
            # get hnmr peak
            url = 'https://sdbs.db.aist.go.jp/sdbs/cgi-bin/' + 'img_disp.cgi'
            data = {}
            old_r = response
            data['imgdir'] = re.search(r'input.*?NAME="imgdir".*?VALUE="(.*?)"', response).group(1)
            data['fname'] = re.search(r'input.*?NAME="fname".*?VALUE="(.*?)"', response).group(1)
            data['disptype'] = re.search(r'input.*?NAME="disptype".*?VALUE="(.*?)"', response).group(1)
            m12 = re.search(r'input.*?NAME="sdbsno".*?VALUE="(.*?)"', response)
            if m12:
                data['sdbsno'] = m12.group(1)

            request = urllib2.Request(url, urllib.urlencode(data), headers)
            response = opener.open(request).read()
            m_disclaimer = is_disclaimer(response)
            if m_disclaimer:
                click_disclaimer(response)
                response = opener.open(request).read()
                m_disclaimer = is_disclaimer(response)
                assert not m_disclaimer, 'ERROR: click disclaimer invalid'+response+sys.exit(1)
            p_pre = re.compile(r'\<pre.*?\>(.*?)\</pre\>', re.MULTILINE | re.DOTALL)
            matches5 = re.finditer(p_pre, response)
            hnmr_details = []
            hnmr_details_pre = ''
            flag = False
            for m11 in matches5:
                l = m11.group(1)
                if re.search(r'Hz\s*ppm\s*Int\.', l):
                    flag = True
                    continue
                if flag:
                    hnmr_details_pre = l.replace('\n','<_newline_>').replace('\t', ' ').strip()
                    items = get_hnmr_details(l.strip(), formula)
                    for i in range(len(items)/3):
                        hnmr_details.append((float(items[i*3]), float(items[i*3+1]), float(items[i*3+2])))
                    break
            print (hnmr_details)
            print (hnmr_details_pre)
            if len(hnmr_details) == 0:
                assert False, 'ERROR: empty hnmr_details'
                continue
            fout.write('%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\n'%(sdbsno, compname, formula, mw, cas, cnmr, hnmr, hnmr_details, cnmr_pre, hnmr_pre, hnmr_details_pre))
            fout.flush()
        except Exception as e:
            print (e)
            traceback.print_exc()

def main():
    html = open_search()
    time.sleep(3)
    cur_page = 1
    mw_from = 12
    mw_to = 100000

    max_pages = 3
    is_last_page = False
    while (not is_last_page) and (cur_page < max_pages):
        try:
            search_html = search(html, mw_from, mw_to, cur_page)
            time.sleep(3)
            read_molecules(search_html)
            m = re.search(r'(\d+)\s*-\s*(\d+)\s*out\s*of\s*(\d+)\s*hits', search_html)
            assert m, 'ERROR: search failed'
            start = int(m.group(1))
            end = int(m.group(2))
            total = int(m.group(3))
            if end >= total:
                is_last_page = True
        except Exception as e:
            print (e)
            traceback.print_exc()
        cur_page += 1
    fout.close()


if __name__ == '__main__':
    # main entry
    main()
