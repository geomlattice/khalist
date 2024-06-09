def rss_item(nadi_stamp, mdlink, post_category):
  return f'''<item>
    <title>{nadi_stamp}l</title>
    <link>{mdlink}</link>
    <description>{post_category}</description>
  </item>
	'''

