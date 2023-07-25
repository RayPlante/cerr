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
			    color: #474747;
			    margin-top: 1em;
			    margin-bottom: 0em !important;
			    font-weight: bolder;
			}
			
			.bigTitle {
			    color: #9eac87;
			    margin-top: 1em;
			    margin-bottom: 0em !important;
			}
			
			.keywordTag {
			    border: 3px double #9eac87;
			    background-color: #f2e4d4;
			    border-radius: 10%;
			    margin-right: 1em;
			    padding: 0 0.8em;
			    margin-bottom: 0;
			    margin-top: 10px;
			}
			
			#resourceContent {
			    display: flex;
			    flex-direction: column;
			    padding: 0em 2em;
			}
			
			#publisherLine p {
			    margin-bottom: 0.5em !important;
			}
			
			#materialTypeDiv {
			}
			
			#lifecyclePhaseDiv {
			    background-color: #9eac87;
			    border: 3px double #f2e4d4;
			}
			
			#productClassDiv {
			
			}
			#infosDetails {
			    width: 60%;
			    margin-bottom: 2em;
			}
			
			#infosDetails > div {
			    margin-top: 1em;
			    padding: 2em 1em;
			    align-items: center;
			    display: flex;
			    flex-flow: row wrap;
			    background-color: #f2e4d4;
			    border-radius: 20px;
			    border: 3px double #9eac87;
			    justify-content: left;
			}
			
			#allContent {
			    display: flex;
			    justify-content: space-around;
			    flex-flow: row wrap;
			}
			#landingPageLink :hover {
			    color: #50672e;
			}
			
			#otherDetails {
			    border: 3px dotted #9eac87;
			    padding: 0em 2em 1em;
			    border-radius: 30px;
			    height: fit-content;
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
		<xsl:variable name="productClass"
			select="//rsm:Resource/rsm:applicability/rsm:productClass/*"/>
		<xsl:variable name="lifecyclePhase"
			select="//rsm:Resource/rsm:applicability/rsm:lifecyclePhase/*"/>
		<xsl:variable name="materialType"
			select="//rsm:Resource/rsm:applicability/rsm:materialType/*"/>

		<div id="resourceContent">
			<xsl:choose>
				<xsl:when test="$title != ''">
					<div id="resourceTitle">
						<h1 class="top1 bigTitle" style="color: #4C5F2E">
							<xsl:value-of select="$title"/>
						</h1>
					</div>
				</xsl:when>
				<xsl:otherwise>
					<strong class="italic top1 title">Untitled</strong>
				</xsl:otherwise>

			</xsl:choose>


			<xsl:if test="$publisher">
				<div id="publisherLine"
					style="display: flex; flex-flow: row wrap; font-size: large; font-style: italic; color: #474747; ">
					<p class="title bold" style="margin-right: 0.5em; margin-top:0em">Published by: </p>
					<p>
						<xsl:value-of select="$publisher"/>
						<xsl:if test="$publicationYear">
							<xsl:text> in </xsl:text>
							<xsl:value-of select="$publicationYear"/>
						</xsl:if>
					</p>
				</div>
			</xsl:if>


			<xsl:if test="$landingPage">
				<span style="font-style: italic">
					<a target="_blank" href="{$landingPage}" id="landingPageLink"
						style="color: #4C5F2E; font-style: normal;">
						<u>View this resource (on external site) </u>
						<sup>
							<i style="font-size: small;" class="fas fa-external-link-alt"/>
						</sup>
						<span style="font-size: xsmall; margin-left: 1em;"><xsl:value-of select="$landingPage"/></span>
					</a>
				</span>
			</xsl:if>


			<xsl:if test="$keywords">
				<!--				<h3 class="title bottom0 bold">Keywords:</h3>-->
				<div style="display: flex; flex-flow: row wrap; margin-top: 1.5em;">
					<xsl:call-template name="split">
						<xsl:with-param name="pText" select="$keywords"/>
					</xsl:call-template>
				</div>
			</xsl:if>


			<xsl:if test="$description">
				<p class="top2">
					<xsl:value-of select="$description"/>
				</p>
			</xsl:if>




			<xsl:if test="$creators">
				<h3 class="title bottom0 bold">Creator:</h3>
				<p>
					<xsl:value-of select="$creators"/>
				</p>
			</xsl:if>

			<div id="allContent">
				<div id="infosDetails">
					<xsl:if test="$materialType">
						<div id="materialTypeDiv">
							<h3 class="title bottom0 bold" style="margin-top:0;   width:30%"
								>Material Type:</h3>
							<div style="display: flex; flex-flow: column wrap">
								<xsl:for-each select="$materialType">
									<span>
										<xsl:copy-of select="."/>
										<!--<xsl:if test="position() != last()">
							<xsl:value-of select="', '"/>
						</xsl:i-->
									</span>
								</xsl:for-each>
							</div>
						</div>
					</xsl:if>

					<xsl:if test="$lifecyclePhase">
						<div id="lifecyclePhaseDiv">
							<h3 class="title bottom0 bold" style="margin-top:0; width:30%">Lifecycle
								Phase:</h3>
							<div style="display: flex; flex-flow: column wrap">
								<xsl:for-each select="$lifecyclePhase">
									<span>
										<xsl:value-of select="."/>
										<!--<xsl:if test="position() != last()">
							<xsl:value-of select="', '"/>
						</xsl:if>-->
									</span>
								</xsl:for-each>
							</div>
						</div>
					</xsl:if>
					
					<xsl:if test="$productClass">
						<div id="productClassDiv">

							<h3 class="title bottom0 bold" style="margin-top:0;  width:30%">Product
								Class:</h3>
							<div style="display: flex; flex-flow: column wrap">
								<xsl:for-each select="$productClass">
									<span>
										<xsl:value-of select="."/>
										<!--<xsl:if test="position() != last()">
							<xsl:value-of select="', '"/>
						</xsl-->
									</span>
								</xsl:for-each>
							</div>
						</div>
					</xsl:if>
				</div>

				<div id="otherDetails">
					<div style="display: flex; flex-flow: column wrap">
						<xsl:if test="$primaryAudience">
							<h3 class="title bottom0 bold" style="text-shadow: 3px 3px 3px #9eac87;">Primary
								Audience:</h3>
							<xsl:for-each select="$primaryAudience">
								<span>
									<xsl:value-of select="."/>
									<!--<xsl:if test="position() != last()">
									<xsl:value-of select="', '"/>
								</xsl:if>-->
								</span>
							</xsl:for-each>
						</xsl:if>
					</div>

					<div style="display: flex; flex-flow: column wrap">
						<xsl:if test="$role">
							<h3 class="title bottom0 bold" style="text-shadow: 3px 3px 3px #9eac87;">Role:</h3>
							<xsl:for-each select="$role">
								<span>
									<xsl:value-of select="."/>
									<!--			<xsl:if test="position() != last()">
										<xsl:value-of select="', '"/>
									</xsl:if>-->
								</span>
							</xsl:for-each>
						</xsl:if>
					</div>
				</div>

			</div>
		</div>
		
		<svg xmlns="//www.w3.org/2000/svg" version="1.1" class="svg-filters" style="display:none;">
			<defs>
				<filter id="marker-shape">
					<feTurbulence type="fractalNoise" baseFrequency="0 0.15" numOctaves="1" result="warp" />
					<feDisplacementMap xChannelSelector="R" yChannelSelector="G" scale="30" in="SourceGraphic" in2="warp" />
				</filter>
			</defs>
		</svg>
	</xsl:template>


	<xsl:template name="split">
		<xsl:param name="pText" select="."/>
		<xsl:variable name="cText"
			select="string-length($pText) - string-length(translate($pText, ',', ''))"/>

		<xsl:if test="string-length($pText) > 0">
			<span class="keywordTag">
				<xsl:value-of select="substring-before(concat($pText, ',', ' '), ',')"/>
				<!--	<xsl:if test="$cText > 0">
					<xsl:value-of select="', '"/>
				</xsl:if>-->
			</span>
			<xsl:call-template name="split">
				<xsl:with-param name="pText" select="substring-after($pText, ',')"/>
			</xsl:call-template>
		</xsl:if>
	</xsl:template>
</xsl:stylesheet>
