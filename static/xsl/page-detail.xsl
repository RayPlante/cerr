<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform" version="1.0"
    xmlns:nr="http://schema.nist.gov/xml/ce-res-md/1.0wd1">
    <xsl:output method="html" indent="yes" encoding="UTF-8" />

	<xsl:template match="/">
    <style>

        div#navigation li {
            list-style: none;
        }

        div#wrapper {
            float: right;
            width: 55%;
        }

        div#navigation {
            float: left;
            width: 45%;
        }

        div#extra {
            clear: both;
            width: 100%;
        }
       	</style>





       	<h1 xmlns:nr="http://schema.nist.gov/xml/ce-res-md/1.0wd1" style="color: #000;font-size: 2.7em;margin-bottom: 10px;"><xsl:value-of select="//nr:Resource/nr:identity/nr:title"/></h1>
       	<xsl:apply-templates select="nr:Resource/nr:providers"/>
		<xsl:apply-templates select="nr:Resource/nr:role"/>
		<xsl:apply-templates select="nr:Resource/nr:content"/>
		<xsl:for-each select="*[name(.)!='description' and name(.)!='subject']">
			<xsl:value-of select="."/>
		</xsl:for-each>
	</xsl:template>


	<xsl:template match="nr:Resource/nr:providers">
		<div id="navigation">
		<xsl:for-each select="./*">
			<xsl:variable name="branchName" select="name(.)" />
			<xsl:variable name="prefix">
				<xsl:choose>
					<xsl:when test="count(ancestor::node())=2"></xsl:when>
					<xsl:otherwise><xsl:value-of select="$branchName"/></xsl:otherwise>
				</xsl:choose>
			</xsl:variable>

			<div>
				<xsl:choose>
					<xsl:when test="count(ancestor::node())=2" >
						<h3 style="letter-spacing: -1px;font-weight: 500;font-size: 1.7em;color: #699BBA; margin: 0.5em 0 0 0">
							<xsl:call-template name="formatText">
								<xsl:with-param name="current" select="$branchName" />
							</xsl:call-template>
						</h3>
					</xsl:when>
				<xsl:otherwise>
				</xsl:otherwise>
				</xsl:choose>

				<xsl:for-each select="*[not(*)]">
				   <xsl:call-template name="leaves">
					  <xsl:with-param name="prefix" select="$prefix"/>
				   </xsl:call-template>
				</xsl:for-each>
			</div>
		</xsl:for-each>

		</div>
	</xsl:template>


	<xsl:template match="nr:Resource/nr:content">
		<div id="extra">
			<xsl:apply-templates select='nr:description'/>
		</div>
	</xsl:template>

	<xsl:template match="nr:Resource/nr:role">
		<div id="wrapper">
			<span style="display:block;color: #888;">
				<xsl:apply-templates select='nr:dataOrigin'/>
			</span>
		</div>
	</xsl:template>

	<xsl:template match="nr:description">
		<span style="letter-spacing: -1px;font-weight: 500;font-size: 1.7em;color: #699BBA; margin: 0.5em 0 0 0">Description</span><br></br>
		<span style="display:block;color: #888;"><strong></strong>
		<xsl:call-template name="formatText">
			<xsl:with-param name="current" select="." />
		</xsl:call-template>
		</span>
	</xsl:template>




















	<xsl:template name="leaves">
		<xsl:param name="prefix" />
		<xsl:variable name="name" select="name(.)" />
		<xsl:variable name="value" select="." />
		<xsl:if test="$value != ''">
			<xsl:choose>
				<xsl:when test="following-sibling::node()[name()=$name] or preceding-sibling::node()[name()=$name]">
					<xsl:choose>
						<xsl:when test="preceding-sibling::node()[name()=$name]" >
						</xsl:when>
						<xsl:otherwise>
							<span style="display:block;color: #888;">
								<strong>
									<xsl:call-template name="formatText">
										<xsl:with-param name="prefix" select="$prefix" />
										<xsl:with-param name="current" select="$name" />
									</xsl:call-template>
									<xsl:text>: </xsl:text>
								</strong>
								<xsl:call-template name="join">
									<xsl:with-param name="current" select="$value" />
									<xsl:with-param name="list" select="following-sibling::node()[name()=$name]" />
									<xsl:with-param name="separator" select="', '" />
								</xsl:call-template>
							</span>
						</xsl:otherwise>
					</xsl:choose>
					<xsl:apply-templates select="@*" />
				</xsl:when>
				<xsl:otherwise>
					<span style="display:block;color: #888;">
						<strong>
							<xsl:call-template name="formatText">
								<xsl:with-param name="prefix" select="$prefix" />
								<xsl:with-param name="current" select="$name" />
							</xsl:call-template>
							<xsl:text>: </xsl:text>
						</strong>
						<xsl:choose>
							<xsl:when test="( (contains($name, 'URL')) or (starts-with($value, 'https://')) or (starts-with($value, 'http://')) )">
								<a target="_blank" href="{$value}"><xsl:value-of select="$value"/></a>
							</xsl:when>
							<xsl:otherwise>
								<xsl:value-of select="$value"/>
							</xsl:otherwise>
						</xsl:choose>
						<xsl:apply-templates select="@*" />
					</span>
				</xsl:otherwise>
			</xsl:choose>
		</xsl:if>
	</xsl:template>

	<xsl:template name="join">
		<xsl:param name="current" />
		<xsl:param name="list" />
		<xsl:param name="separator"/>

		<xsl:value-of select="$current" />
		<xsl:apply-templates select="@*" />
		<xsl:value-of select="$separator" />

		<xsl:for-each select="$list">
			<xsl:value-of select="." />
			<xsl:apply-templates select="@*" />
			<xsl:if test="position() != last()">
				<xsl:value-of select="$separator" />
			</xsl:if>
		</xsl:for-each>
	</xsl:template>

	<xsl:template name="formatText">
		<xsl:param name="prefix" />
		<xsl:param name="current" />
		<xsl:variable name="uppercase" select="'ABCDEFGHIJKLMNOPQRSTUVWXYZ'"/>
		<xsl:variable name="lowercase" select="'abcdefghijklmnopqrstuvwxyz'"/>

		<xsl:variable name="upperPrefix" select="concat(translate(substring($prefix, 1, 1), $lowercase, $uppercase), substring($prefix, 2))"/>
		<xsl:variable name="upperCurrent" select="concat(translate(substring($current, 1, 1), $lowercase, $uppercase), substring($current, 2))"/>
		<xsl:call-template name="SplitCamelCase">
			<xsl:with-param name="text" select="concat($upperPrefix,$upperCurrent)" />
		</xsl:call-template>
	</xsl:template>

	<xsl:template name="SplitCamelCase">
		<xsl:param name="text" />
		<xsl:param name="digitsMode" select="0" />
		<xsl:variable name="upper" select="'ABCDEFGHIJKLMNOPQRSTUVWXYZ'"/>
		<xsl:variable name="lower" select="'abcdefghijklmnopqrstuvwxyz'"/>
		<xsl:variable name="digits">0123456789</xsl:variable>

		<xsl:if test="$text != ''">
			<xsl:variable name="letter" select="substring($text, 1, 1)" />
			<xsl:variable name="followingLetter" select="substring($text, 2, 2)" />
			<xsl:choose>
				<xsl:when test="(contains($upper, $letter) and not(contains($upper, $followingLetter)))">
					<xsl:text> </xsl:text>
					<xsl:value-of select="$letter" />
				</xsl:when>
				<xsl:when test="contains($digits, $letter)">
					<xsl:choose>
						<xsl:when test="$digitsMode != 1">
							<xsl:text> </xsl:text>
						</xsl:when>
					</xsl:choose>
					<xsl:value-of select="$letter" />
				</xsl:when>
				<xsl:otherwise>
					<xsl:value-of select="$letter"/>
				</xsl:otherwise>
			</xsl:choose>
			<xsl:call-template name="SplitCamelCase">
				<xsl:with-param name="text" select="substring-after($text, $letter)" />
				<xsl:with-param name="digitsMode" select="contains($digits, $letter)" />
			</xsl:call-template>
		</xsl:if>
	</xsl:template>

	<xsl:template match="@*">
		<xsl:variable name="name" select="name(.)" />
		<xsl:variable name="value" select="." />
		<xsl:if test="$value != ''">
			<xsl:if test="not(starts-with($name, 'xsi:type'))">
				<span class='value'>
					<xsl:text> (</xsl:text>
					<xsl:value-of select="$name" /> <xsl:text>: </xsl:text>
					<xsl:choose>
						<xsl:when test="( (contains($name, 'URL')) or (starts-with($value, 'https://')) or (starts-with($value, 'http://')) )">
							<a target="_blank" href="{$value}"><xsl:value-of select="$value"/></a>
						</xsl:when>
						<xsl:otherwise>
							<xsl:value-of select="$value"/>
						</xsl:otherwise>
					</xsl:choose>
					<xsl:text>)</xsl:text>
				</span>
			</xsl:if>
		</xsl:if>
	</xsl:template>
</xsl:stylesheet>
