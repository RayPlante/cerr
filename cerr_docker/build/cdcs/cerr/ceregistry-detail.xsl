<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
	xmlns:xs="http://www.w3.org/2001/XMLSchema"
	xmlns:rsm="http://schema.nist.gov/xml/ce-res-md/1.0wd2"
	xmlns:am="http://schema.nist.gov/xml/nmrr.schema.annot"
	xmlns:ghgr="https://data.nist.gov/od/dm/ghgr/v1.0exp" xmlns:exsl="http://exslt.org/common"
	version="1.0" exclude-result-prefixes="exsl">

	<xsl:output method="html" indent="yes" encoding="UTF-8"/>
	<xsl:template match="/">

		<style>
			
			.top2 {
			    margin-top: 2em;
			}
			
			.title {
			    color: #9eac87;
			    margin-top: 1em;
			    margin-bottom: 0em;
			    font-weight: bolder;
			}
			
			.bigTitle {
			    color: #474747;
			    margin-top: 1em;
			}
			
		</style>

		<xsl:variable name="title" select="//rsm:Resource/rsm:identity/rsm:title"/>
		<xsl:variable name="keywords" select="//rsm:Resource/rsm:content/rsm:subject"/>
		<xsl:variable name="description" select="//rsm:Resource/rsm:content/rsm:description"/>
		<xsl:variable name="landingPage" select="//rsm:Resource/rsm:content/rsm:landingPage"/>
		<xsl:variable name="primaryAudience" select="//rsm:Resource/rsm:content/rsm:primaryAudience"/>
		<xsl:variable name="creators" select="//rsm:Resource/rsm:providers/rsm:contact/rsm:name"/>
		<xsl:variable name="publisher" select="//rsm:Resource/rsm:providers/rsm:publisher"/>
		<xsl:variable name="publicationYear"
			select="//rsm:Resource/rsm:providers/rsm:publicationYear"/>
		<xsl:variable name="role" select="//rsm:Resource/rsm:role/rsm:type"/>
		<xsl:variable name="productClass" select="//rsm:Resource/rsm:applicability/rsm:productClass/*"/>
		<xsl:variable name="lifecyclePhase"
			select="//rsm:Resource/rsm:applicability/rsm:lifecyclePhase/*"/>
		<xsl:variable name="materialType" select="//rsm:Resource/rsm:applicability/rsm:materialType/*"/>

		<xsl:choose>
			<xsl:when test="$title != ''">
				<h1 class="top1 bigTitle">
					<xsl:value-of select="$title"/>
				</h1>
			</xsl:when>
			<xsl:otherwise>
				<strong class="italic top1 title">Untitled</strong>
			</xsl:otherwise>
		</xsl:choose>



		<xsl:if test="$landingPage">
			<h3 class="top2">
				<a target="_blank" href="{$landingPage}" style="color: #9eac87; font-style: normal;">
					<u>View this resource (on external site) </u>
					<sup>
						<i style="font-size: small;" class="fas fa-external-link-alt"/>
					</sup>
				</a>
			</h3>
		</xsl:if>


		<xsl:if test="$description">
			<p class="top2">
				<xsl:value-of select="$description"/>
			</p>
		</xsl:if>


		<xsl:if test="$keywords">
			<h3 class="title bottom0 bold">Keywords:</h3>
			<xsl:call-template name="split">
				<xsl:with-param name="pText" select="$keywords"/>
			</xsl:call-template>
		</xsl:if>


		<xsl:if test="$creators">
			<h3 class="title bottom0 bold">Creator:</h3>
			<p>
				<xsl:value-of select="$creators"/>
			</p>
		</xsl:if>


		<xsl:if test="$publisher">
			<h3 class="title bottom0 bold">Published by: </h3>
			<xsl:value-of select="$publisher"/>
			<xsl:if test="$publicationYear">
				<xsl:text> in </xsl:text>
				<xsl:value-of select="$publicationYear"/>
			</xsl:if>
		</xsl:if>
		

		<xsl:if test="$primaryAudience">
			<h3 class="title bottom0 bold">Primary Audience:</h3>
			<xsl:for-each select="$primaryAudience">
				<span>
					<xsl:value-of select="."/>
					<xsl:if test="position() != last()">
						<xsl:value-of select="', '"/>
					</xsl:if>
				</span>
			</xsl:for-each>
		</xsl:if>


		<xsl:if test="$role">
			<h3 class="title bottom0 bold">Role:</h3>
			<xsl:for-each select="$role">
				<span>
					<xsl:value-of select="."/>
					<xsl:if test="position() != last()">
						<xsl:value-of select="', '"/>
					</xsl:if>
				</span>
			</xsl:for-each>
		</xsl:if>


		<xsl:if test="$materialType">
			<h3 class="title bottom0 bold">Material Type:</h3>
			<xsl:for-each select="$materialType">
				<span>
					<xsl:copy-of select="."/>
					<xsl:if test="position() != last()">
						<xsl:value-of select="', '"/>
					</xsl:if>
				</span>
			</xsl:for-each>
		</xsl:if>


		<xsl:if test="$lifecyclePhase">
			<h3 class="title bottom0 bold">Lifecycle Phase:</h3>
			<xsl:for-each select="$lifecyclePhase">
				<span>
					<xsl:value-of select="."/>
					<xsl:if test="position() != last()">
						<xsl:value-of select="', '"/>
					</xsl:if>
				</span>
			</xsl:for-each>
		</xsl:if>


		<xsl:if test="$productClass">
			<h3 class="title bottom0 bold">Product Class:</h3>
			<xsl:for-each select="$productClass">
				<span>
					<xsl:value-of select="."/>
					<xsl:if test="position() != last()">
						<xsl:value-of select="', '"/>
					</xsl:if>
				</span>
			</xsl:for-each>
		</xsl:if>


	</xsl:template>


	<xsl:template name="split">
		<xsl:param name="pText" select="."/>
		<xsl:variable name="cText"
			select="string-length($pText) - string-length(translate($pText, ',', ''))"/>

		<xsl:if test="string-length($pText) > 0">
			<xsl:value-of select="substring-before(concat($pText, ',', ' '), ',')"/>
			<xsl:if test="$cText > 0">
				<xsl:value-of select="', '"/>
			</xsl:if>
			<xsl:call-template name="split">
				<xsl:with-param name="pText" select="substring-after($pText, ',')"/>
			</xsl:call-template>
		</xsl:if>
	</xsl:template>
</xsl:stylesheet>
