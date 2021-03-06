<?xml version="1.0" encoding="UTF-8"?>

<xsl:stylesheet version="1.0"
xmlns:xsl="http://www.w3.org/1999/XSL/Transform">

<xsl:template match="/">
  <html>
  <body>
  <h2>Hotline products</h2>
  <table border="2px solid black">
    <tr bgcolor="#9acd32">
      <th>Price</th>
      <th>Description</th>
      <th>Image</th>
    </tr>
    <xsl:for-each select="data/product">
    <tr>
      <td style="text-align:center"><xsl:value-of select="price"/></td>
      <td style="text-align:center"><xsl:value-of select="description"/></td>
      <td style="text-align:center">

	<img>
	    <xsl:attribute name="src">
		<xsl:value-of select="image"/>
	    </xsl:attribute>
	</img>
	</td>
    </tr>
    </xsl:for-each>
  </table>
  </body>
  </html>
</xsl:template>

</xsl:stylesheet>
