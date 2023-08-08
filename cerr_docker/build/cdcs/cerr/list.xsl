<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
    xmlns:xs="http://www.w3.org/2001/XMLSchema"
    xmlns:rsm="http://schema.nist.gov/xml/ce-res-md/1.0wd2"
    xmlns:am="http://schema.nist.gov/xml/nmrr.schema.annot"
    xmlns:ghgr="https://data.nist.gov/od/dm/ghgr/v1.0exp" xmlns:exsl="http://exslt.org/common"
    exclude-result-prefixes="exsl">
    <xsl:output method="html" indent="yes" encoding="UTF-8"/>


    <xsl:template match="/">

        <style>
            div[name = "result"] a,
            div[name = "result"] a:link {
                color: #4C5F2E;
            }
            
            div[name = "result"]:hover a,
            div[name = "result"]:hover a:link {
                opacity: 0.5;
            }</style>

        <div class="container-fluid" style="background-color: #f2e4d4;
            border-radius: 1em;
            padding: .5em 1.5em;
            margin-bottom: .25em;
            margin-top: .25em;">
            <div class="row" style="margin-top: 0;">
                <div class="col-lg" style="display: flex; align-items: center; padding-top: 0;">
                    <div class="col-lg">

                        <xsl:variable name="title" select="//rsm:Resource/rsm:identity/rsm:title"/>
                        <xsl:text disable-output-escaping="yes">&lt;a class="title" href="</xsl:text>
                        <xsl:text disable-output-escaping="yes">{{ result.detail_url }}</xsl:text>
                        <xsl:text disable-output-escaping="yes">" &gt;</xsl:text>
                        <xsl:choose>
                            <xsl:when test="$title != ''">
                                <strong>
                                    <xsl:value-of select="$title"/>
                                </strong>
                            </xsl:when>
                            <xsl:otherwise>
                                <strong class="italic">Untitled</strong>
                            </xsl:otherwise>
                        </xsl:choose>
                        <xsl:text disable-output-escaping="yes">&lt;/a&gt;</xsl:text>
                        <xsl:variable name="creators"
                            select="//rsm:Resource/rsm:providers/rsm:contact/rsm:name"/>
                        <xsl:variable name="publisher"
                            select="//rsm:Resource/rsm:providers/rsm:publisher"/>
                        <xsl:if test="(($creators != '') or ($publisher != ''))">
                            <xsl:text> - </xsl:text>
                        </xsl:if>
                        <xsl:call-template name="join">
                            <xsl:with-param name="list" select="$creators"/>
                            <xsl:with-param name="separator" select="', '"/>
                        </xsl:call-template>
                        <xsl:if test="(($creators != '') and ($publisher != ''))">
                            <xsl:text> - </xsl:text>
                        </xsl:if>
                        <xsl:value-of select="$publisher"/>
                        <xsl:variable name="subject" select="//rsm:Resource/rsm:content/rsm:subject"/>
                        <xsl:variable name="total"
                            select="string-length($subject) - string-length(translate($subject, ',', ''))"/>

                        <xsl:if test="$subject != ''">
                            <div class="keywords"
                                style="line-height: 1.1em; margin-top:0.5em; margin-bottom:0.25em;">
                                <xsl:text>Subject keyword(s): </xsl:text>
                                <xsl:call-template name="split">
                                    <xsl:with-param name="pText" select="$subject"/>
                                    <xsl:with-param name="total" select="$total"/>
                                </xsl:call-template>
                            </div>
                        </xsl:if>

                        <div class="black" style="line-height: 1.1em;">
                            <p class="description">
                                <xsl:value-of select="//rsm:Resource/rsm:content/rsm:description"/>
                            </p>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </xsl:template>

    <xsl:template name="join">
        <xsl:param name="list"/>
        <xsl:param name="separator"/>

        <xsl:for-each select="$list">
            <xsl:value-of select="."/>
            <xsl:if test="position() != last()">
                <xsl:value-of select="$separator"/>
            </xsl:if>
        </xsl:for-each>
    </xsl:template>

    <xsl:template match="//*[not(*)]">
        <xsl:variable name="name" select="name(.)"/>
        <xsl:variable name="value" select="."/>
        <xsl:variable name="arg" select="@type"/>
        <xsl:if
            test="((contains($name, 'URL')) or (starts-with($value, 'https://')) or (starts-with($value, 'http://')))">
            <xsl:if test="$value != ''">
                <xsl:value-of select="$name"/>
                <xsl:text>: </xsl:text>
                <a target="_blank" href="{$value}">
                    <xsl:value-of select="$value"/>
                </a>
                <br/>
            </xsl:if>
        </xsl:if>
    </xsl:template>

    <xsl:template match="ghgr:homePage">
        <xsl:choose>
            <xsl:when test="ghgr:doi">
                <xsl:variable name="url">https://doi.org/<xsl:value-of select="ghgr:doi"
                    /></xsl:variable>
                <a target="_blank" href="{$url}">doi:<xsl:value-of select="ghgr:doi"/></a>
            </xsl:when>
            <xsl:when test="ghgr:url">
                <a target="_blank" href="{ghgr:url}">URL: <xsl:value-of select="ghgr:url"/></a>
            </xsl:when>
            <xsl:otherwise>
                <i>No Home Page URL provided</i>
            </xsl:otherwise>
        </xsl:choose>
    </xsl:template>


    <xsl:template name="split">
        <xsl:param name="pText" select="."/>
        <xsl:param name="total"/>
        <xsl:variable name="cText"
            select="string-length($pText) - string-length(translate($pText, ',', ''))"/>
        <xsl:if test="string-length($pText) > 0 and (number($total) - $cText) &lt; 3">
            <xsl:value-of select="substring-before(concat($pText, ',', ' '), ',')"/>
            <xsl:if test="$cText > 0 and (number($total) - $cText) &lt; 2">
                <xsl:value-of select="', '"/>
            </xsl:if>
            <xsl:call-template name="split">
                <xsl:with-param name="pText" select="substring-after($pText, ',')"/>
                <xsl:with-param name="total" select="$total"/>
            </xsl:call-template>
        </xsl:if>
    </xsl:template>



</xsl:stylesheet>
