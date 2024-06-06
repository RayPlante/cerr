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
                color: black;
                margin-bottom: 0em !important;
                font-weight: bolder;
            }
            .bigTitle {
                color: #9eac87;
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
                color: black;
            }
            #publisherLine p {
                margin-bottom: 0.5em !important;
            }
            #materialTypeDiv {
            }
            #lifecyclePhaseDiv {
            }
            #productClassDiv {
            }
            #infosDetails {
                width: 60%;
                margin-bottom: 2em;
                margin-top: 1em
            }
            #infosDetails > div {
                margin-top: 1em;
                padding: 1em;
                align-items: flex-start;
                display: flex;
                flex-flow: column wrap;
                border-radius: 20px;
                border: 3px double #9eac87;
                justify-content: space-evenly;
                max-width: 80%;
                font-size: 1em;
            }<!--background-color: #f2e4d4;-->
            #allContent {
                display: flex;
                flex-flow: column wrap;
                margin-top: 1em;
            }
            #landingPageBtn {
                background-color: #9eac87;
                color: black;
                font-size: large;
                margin: 0.5em;
                padding: 0.5em;
            }
            #landingPageBtn:hover {
                background-color: #9eac87 !important;
                opacity: 0.7;
            }
            #otherDetails {
                border-radius: 30px;
                height: fit-content;
                margin-top: 1em;
            }
            
            #exploreLink:hover #shortLink {
                display: none
            }
            
            #exploreLink:hover #longLink {
                display: block !important
            }</style>


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

        <xsl:variable name="eventStartDate" select="//rsm:Resource/rsm:content/rsm:startDate"/>
        <xsl:variable name="eventEndDate" select="//rsm:Resource/rsm:content/rsm:endDate"/>
        <xsl:variable name="eventOnline" select="//rsm:Resource/rsm:content/rsm:event_online"/>
        <xsl:variable name="eventVenue" select="//rsm:Resource/rsm:content/rsm:venue"/>
        <xsl:variable name="eventRecurring" select="//rsm:Resource/rsm:content/rsm:eventRecurring"/>

        <div id="resourceContent">
            <div style="display: flex; flex-flow: column wrap">
                <xsl:if test="$role">
                    <xsl:for-each select="$role">
                        <span style="display:inline; font-size: larger">
                            <xsl:if test="starts-with(., 'Literature')">
                                <i style="font-size: small; margin-right: 1em;" class="fas fa-book"
                                />
                            </xsl:if>
                            <xsl:if test="starts-with(., 'Dataset')">
                                <i style="font-size: small; margin-right: 1em;"
                                    class="fas fa-database"/>
                            </xsl:if>
                            <xsl:if test="starts-with(., 'Tool')">
                                <i style="font-size: small; margin-right: 1em;" class="fas fa-cogs"
                                />
                            </xsl:if>
                            <xsl:if test="starts-with(., 'Organization')">
                                <i style="font-size: small; margin-right: 1em;"
                                    class="fas fa-university"/>
                            </xsl:if>
                            <xsl:if test="starts-with(., 'Website')">
                                <i style="font-size: small; margin-right: 1em;"
                                    class="fas fa-laptop"/>
                            </xsl:if>
                            <xsl:if test="starts-with(., 'Collection')">
                                <i style="font-size: small; margin-right: 1em;" class="fas fa-table"
                                />
                            </xsl:if>
                            <xsl:if test="starts-with(., 'Event')">
                                <i style="font-size: small; margin-right: 1em;"
                                    class="fas fa-calendar"/>
                            </xsl:if>
                            <xsl:value-of select="."/>
                        </span>
                    </xsl:for-each>
                </xsl:if>
            </div>
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
                    style="display: flex; flex-flow: row wrap;; font-style: italic; margin-top:1em">
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
                <div style="display:flex; flex-wrap: nowrap; align-items: center;" id="exploreLink" >

                    <span style="font-style: italic">
                        <a target="_blank" rel="noopener noreferrer" href="{$landingPage}"
                            id="landingPageLink" style="font-style: large; font-weight: bold;">
                            <button type="button" class="btn btn-primary btn-lg" id="landingPageBtn">
                                <u>Explore resource</u>
                                <sup>
                                    <i style="font-size: small; margin-left:0.5em;"
                                        class="fas fa-external-link-alt"/>
                                </sup>
                            </button>
                        </a>
                    </span>
                    <xsl:call-template name="cutLink">
                        <xsl:with-param name="link" select="$landingPage"/>
                    </xsl:call-template>

                    <!--    
                 
                    <span style="font-size: medium; margin-left: 1em;font-style: italic;">
                        <xsl:value-of select="$landingPage"/>
                    </span>
               -->
                </div>
            </xsl:if>
            <xsl:if test="$description">
                <p class="top2">
                    <xsl:value-of select="$description" disable-output-escaping="yes"/>
                </p>
            </xsl:if>
            <xsl:if test="$keywords">
                <h5 class="title bottom0 bold ">Keywords:</h5>
                <div style="display: flex; flex-flow: row wrap;">
                    <xsl:call-template name="split">
                        <xsl:with-param name="pText" select="$keywords"/>
                    </xsl:call-template>
                </div>
            </xsl:if>

            <div id="allContent">
                <div id="otherDetails">

                    <xsl:if test="$primaryAudience">
                        <h5 class="title bottom0 bold">
                            <!--style="text-shadow: 3px 3px 3px #9eac87;"--> Primary Audience:</h5>
                        <div style="display: flex; flex-flow: row wrap">
                            <xsl:for-each select="$primaryAudience">
                                <span class="keywordTag">
                                    <xsl:value-of select="."/>
                                    <!--<xsl:if test="position() != last()"><xsl:value-of select="', '"/></xsl:if>-->
                                </span>
                            </xsl:for-each>
                        </div>
                    </xsl:if>
                    <xsl:if test="starts-with($role, 'Event')">
                        <xsl:if test="$eventStartDate">

                            <span>This event starts on <xsl:value-of select="$eventStartDate"
                                /></span>

                        </xsl:if>
                        <xsl:if test="$eventEndDate">
                            <span> and ends on <xsl:value-of select="$eventEndDate"/>
                            </span>
                        </xsl:if>
                        <xsl:if test="$eventOnline">

                            <span> This is event is <xsl:value-of select="$eventOnline"/>
                            </span>
                        </xsl:if>
                        <xsl:if test="$eventVenue">
                            <span> and ou can access it at / through <xsl:value-of
                                    select="$eventVenue"/></span>
                        </xsl:if>
                        <xsl:if test="$eventRecurring">
                            <span>(This is a recurring event) </span>
                        </xsl:if>
                    </xsl:if>
                    <xsl:if test="$creators">
                        <h3 class="title bottom0 bold">Creator:</h3>
                        <p>
                            <xsl:value-of select="$creators"/>
                        </p>
                    </xsl:if>
                </div>
                <div id="infosDetails">
                    <xsl:if test="$materialType">
                        <div id="materialTypeDiv">
                            <span class="title bottom0 bold" style="margin-top:0;">Material Types
                                involved:</span>
                            <div style="display: flex; flex-flow: column wrap;  margin-top:1em">
                                <xsl:for-each select="$materialType">
                                    <li>
                                        <xsl:copy-of select="."/>
                                        <!--<xsl:if test="position() != last()"><xsl:value-of select="', '"/></xsl:i-->
                                    </li>
                                </xsl:for-each>
                            </div>
                        </div>
                    </xsl:if>
                    <xsl:if test="$lifecyclePhase">
                        <div id="lifecyclePhaseDiv">
                            <span class="title bottom0 bold" style="margin-top:0;"> Lifecycle phase
                                involved:</span>
                            <div style="display: flex; flex-flow: column wrap; margin-top:1em">
                                <xsl:for-each select="$lifecyclePhase">
                                    <li>
                                        <xsl:value-of select="."/>
                                        <!--<xsl:if test="position() != last()"><xsl:value-of select="', '"/></xsl:if>-->
                                    </li>
                                </xsl:for-each>
                            </div>
                        </div>
                    </xsl:if>
                    <xsl:if test="$productClass">
                        <div id="productClassDiv">
                            <span class="title bottom0 bold" style="margin-top:0;">Relates to these
                                product classes:</span>
                            <div style="display: flex; flex-flow: column wrap; margin-top:1em">
                                <xsl:for-each select="$productClass">
                                    <li style="font-size;medium">
                                        <xsl:value-of select="."/>
                                        <!--<xsl:if test="position() != last()"><xsl:value-of select="', '"/></xsl-->
                                    </li>
                                </xsl:for-each>
                            </div>
                        </div>
                    </xsl:if>
                </div>

            </div>
        </div>
        <svg xmlns="//www.w3.org/2000/svg" version="1.1" class="svg-filters" style="display:none;">
            <defs>
                <filter id="marker-shape">
                    <feTurbulence type="fractalNoise" baseFrequency="0 0.15" numOctaves="1"
                        result="warp"/>
                    <feDisplacementMap xChannelSelector="R" yChannelSelector="G" scale="30"
                        in="SourceGraphic" in2="warp"/>
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
                <!--<xsl:if test="$cText > 0"><xsl:value-of select="', '"/></xsl:if>-->
            </span>
            <xsl:call-template name="split">
                <xsl:with-param name="pText" select="substring-after($pText, ',')"/>
            </xsl:call-template>
        </xsl:if>
    </xsl:template>
    <xsl:template name="cutLink">
        <xsl:param name="link" select="."/>
        <xsl:variable name="domain"
            select="substring-before(substring-after(substring-after($link, '/'), '/'), '/')"/>
        <xsl:choose>
            <xsl:when test="contains($link, 'https://doi.org/')">
                <span style="font-size: medium; margin-left: 1em;font-style: italic;">
                    <xsl:value-of select="$link"/>
                </span>
            </xsl:when>

            <xsl:when test="string-length($domain) > 0">
                <span style="font-size: medium; margin-left: 1em;font-style: italic;"
                    id="shortLink">
                    <xsl:value-of
                        select="concat(substring-before($link, '//'), '//', $domain, '/...')"/>
                </span>
                <span style="font-size: medium; margin-left: 1em;font-style: italic; display:none"
                    id="longLink">
                    <xsl:value-of select="$link"/>
                </span>
            </xsl:when>
            
            <xsl:otherwise>
                <span style="font-size: medium; margin-left: 1em;font-style: italic;">
                    <xsl:value-of select="$link"/>
                </span>
            </xsl:otherwise>
        </xsl:choose>
    </xsl:template>

</xsl:stylesheet>
