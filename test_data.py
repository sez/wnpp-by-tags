# wnpp-by-tags - query WNPP bugs using the debtags of their packages
# Copyright (C) 2009 Serafeim Zanikolas <serzan@hellug.gr>
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA

orphaned_raw_data = \
"""<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01//EN" "http://www.w3.org/TR/html4/strict.dtd">
<html lang="en">
<head>
  <meta http-equiv="Content-Type" content="text/html; charset=iso-8859-1">
  <title>Debian -- Orphaned packages </title>
  <link rev="made" href="mailto:webmaster@debian.org">
  <meta name="Generator" content="WML 2.0.11 (19-Aug-2006)">
  <meta name="Modified" content="2009-05-27 19:28:37">
<link href="../../debian.css" rel="stylesheet" type="text/css">
  <link href="../../debian-en.css" rel="stylesheet" type="text/css" media="all">
</head>
<body>
<div id="header">
   <div id="upperheader">
   <div id="logo">
  <a href="../../"><img src="../../logos/openlogo-nd-50.png" width="50" height="61" alt=""></a>
  <a href="../../" rel="start"><img src="../../Pics/debian.png" width="179" height="61" alt="Debian Project"></a>
  </div> <!-- end logo -->
<div id="serverselect">
<!--UdmComment-->
<form method="get" action="http://cgi.debian.org/cgi-bin/redirect.pl">
<p>
<input type="hidden" name="page" value="/devel/wnpp/orphaned">
Select a server near you
<br>
<select name="site">
<option value="au">Australia</option>
<option value="at">Austria</option>
<option value="br">Brazil</option>
<option value="bg">Bulgaria</option>
<option value="cn">China</option>
<option value="fr">France</option>
<option value="de">Germany</option>
<option value="hk">Hong Kong</option>
<option value="id">Indonesia</option>
<option value="jp">Japan</option>
<option value="nl">Netherlands</option>
<option value="ru">Russia</option>
<option value="za">South Africa</option>
<option value="es">Spain</option>
<option value="ua">Ukraine</option>
<option value="uk">United Kingdom</option>
<option value="us" selected>United States</option>
</select>
<input type="submit" value=" Go ">
</p>
</form>
<!--/UdmComment-->
</div> <!-- end serverselect -->
</div> <!-- end upperheader -->
<!--UdmComment-->
<div id="navbar">
<p class="hidecss"><a href="#inner">Skip Quicknav</a></p>
<ul>
   <li><a href="../../intro/about">About Debian</a></li>
   <li><a href="../../News/">News</a></li>
   <li><a href="../../distrib/">Getting Debian</a></li>
   <li><a href="../../support">Support</a></li>
   <li><a href="../../devel/">Developers'&nbsp;Corner</a></li>
   <li><a href="../../sitemap">Site map</a></li>
   <li><a href="http://search.debian.org/">Search</a></li>
</ul>
</div> <!-- end navbar -->
</div> <!-- end header -->
<!--/UdmComment-->
<div id="outer">
<div id="inner">
<h1>Orphaned packages</h1>
<ul><li><a href="http://bugs.debian.org/525488">9menu: Creates X menus from the shell</a>  (<a href="http://packages.debian.org/src:9menu">package info</a>) </li>
 <li><a href="http://bugs.debian.org/503554">a2ps-perl-ja: perl version of Miguel Santana&#39;s a2ps (supports KANJI)</a>  (<a href="http://packages.debian.org/src:a2ps-perl-ja">package info</a>) </li>
 <li><a href="http://bugs.debian.org/525446">aap: make-like &quot;expert system&quot; for building software</a>  (<a href="http://packages.debian.org/src:aap">package info</a>) </li>
</ul>
<div class="clr"></div>
</div> <!-- end inner -->
<div id="footer">
<hr class="hidecss">
<p>Back to the <a href="../../">Debian Project homepage</a>.</p>
<hr>
<hr>
<div id="fineprint">
  <p>To report a problem with the web site, e-mail <a href="mailto:debian-www@lists.debian.org">debian-www@lists.debian.org</a>. For other contact information, see the Debian <a href="../../contact">contact page</a>.</p>
<p>
Last Modified: Wed, May 27 19:28:37 UTC 2009
  <br>
  Copyright &copy; 1997-2009
 <a href="http://www.spi-inc.org/">SPI</a>; See <a href="../../license" rel="copyright">license terms</a><br>
  Debian is a registered <a href="../../trademark">trademark</a> of Software in the Public Interest, Inc.
</p>
</div>
</div> <!-- end footer -->
</div> <!-- end outer -->
</body>
</html>"""

rfa_raw_data = \
"""
<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01//EN" "http://www.w3.org/TR/html4/strict.dtd">
<html lang="en">
<head>
  <meta http-equiv="Content-Type" content="text/html; charset=iso-8859-1">
  <title>Debian -- Packages up for adoption </title>
  <link rev="made" href="mailto:webmaster@debian.org">
  <meta name="Generator" content="WML 2.0.11 (19-Aug-2006)">
  <meta name="Modified" content="2009-05-27 19:28:42">
<link href="../../debian.css" rel="stylesheet" type="text/css">
  <link href="../../debian-en.css" rel="stylesheet" type="text/css" media="all">
</head>
<body>
<div id="header">
   <div id="upperheader">
   <div id="logo">
  <a href="../../"><img src="../../logos/openlogo-nd-50.png" width="50" height="61" alt=""></a>
  <a href="../../" rel="start"><img src="../../Pics/debian.png" width="179" height="61" alt="Debian Project"></a>
  </div> <!-- end logo -->
<div id="serverselect">
<!--UdmComment-->
<form method="get" action="http://cgi.debian.org/cgi-bin/redirect.pl">
<p>
<input type="hidden" name="page" value="/devel/wnpp/rfa_bypackage">
Select a server near you
<br>
<select name="site">
<option value="au">Australia</option>
<option value="at">Austria</option>
<option value="br">Brazil</option>
<option value="bg">Bulgaria</option>
<option value="cn">China</option>
<option value="fr">France</option>
<option value="de">Germany</option>
<option value="hk">Hong Kong</option>
<option value="id">Indonesia</option>
<option value="jp">Japan</option>
<option value="nl">Netherlands</option>
<option value="ru">Russia</option>
<option value="za">South Africa</option>
<option value="es">Spain</option>
<option value="ua">Ukraine</option>
<option value="uk">United Kingdom</option>
<option value="us" selected>United States</option>
</select>
<input type="submit" value=" Go ">
</p>
</form>
<!--/UdmComment-->
</div> <!-- end serverselect -->
</div> <!-- end upperheader -->
<!--UdmComment-->
<div id="navbar">
<p class="hidecss"><a href="#inner">Skip Quicknav</a></p>
<ul>
   <li><a href="../../intro/about">About Debian</a></li>
   <li><a href="../../News/">News</a></li>
   <li><a href="../../distrib/">Getting Debian</a></li>
   <li><a href="../../support">Support</a></li>
   <li><a href="../../devel/">Developers'&nbsp;Corner</a></li>
   <li><a href="../../sitemap">Site map</a></li>
   <li><a href="http://search.debian.org/">Search</a></li>
</ul>
</div> <!-- end navbar -->
</div> <!-- end header -->
<!--/UdmComment-->
<div id="outer">
<div id="inner">
<h1>Packages up for adoption</h1>
<ul>
<li><a href="http://bugs.debian.org/475377">afnix: Compiler and run-time for the AFNIX programming language</a>  (<a href="http://packages.debian.org/src:afnix">package info</a>) </li>
<li><a href="http://bugs.debian.org/517341">alsaplayer: PCM player designed for ALSA</a>  (<a href="http://packages.debian.org/src:alsaplayer">package info</a>) </li>
<li><a href="http://bugs.debian.org/516255">azureus: BitTorrent client</a>  (<a href="http://packages.debian.org/src:azureus">package info</a>) </li>
<li><a href="http://bugs.debian.org/447393">bins: Generate static HTML photo albums using XML and EXIF tags</a>  (<a href="http://packages.debian.org/src:bins">package info</a>) </li>
</ul>
<div class="clr"></div>
</div> <!-- end inner -->
<div id="footer">
<hr class="hidecss">
<p>Back to the <a href="../../">Debian Project homepage</a>.</p>
<hr>
<hr>
<div id="fineprint">
  <p>To report a problem with the web site, e-mail <a href="mailto:debian-www@lists.debian.org">debian-www@lists.debian.org</a>. For other contact information, see the Debian <a href="../../contact">contact page</a>.</p>
<p>
Last Modified: Wed, May 27 19:28:42 UTC 2009
  <br>
  Copyright &copy; 1997-2009
 <a href="http://www.spi-inc.org/">SPI</a>; See <a href="../../license" rel="copyright">license terms</a><br>
  Debian is a registered <a href="../../trademark">trademark</a> of Software in the Public Interest, Inc.
</p>
</div>
</div> <!-- end footer -->
</div> <!-- end outer -->
</body>
</html>
"""

popcon_raw_data = \
"""
Package: bins                              29   151     5     0
Package: aap                               12    42    26     0
Package: azureus                          886  1415   188     1
Package: afnix                              2     5     3     0
Package: alsaplayer                         0     0     0   129
Package: a2ps-perl-ja                      28    99    32     0
"""
