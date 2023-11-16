import responses
from click.testing import CliRunner

from wadalize import WADLHandler
from wadalize.scripts.wadalize import run as wadalize


WADL_SAMPLE = """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<application xmlns="http://research.sun.com/wadl/2006/10">
    <doc xmlns:jersey="http://jersey.java.net/" jersey:generatedBy="Jersey:
        1.8 06/24/2011 12:17 PM"/>
    <resources base="https://some.sub.example.com">
        <resource path="/{endpoint:stats|summary}/{jobId}">
            <method name="GET" id="getMethod">
                <request>
                    <param xmlns:xs="http://www.w3.org/2001/XMLSchema" type="xs:string" style="query" name="q"/>
                    <param xmlns:xs="http://www.w3.org/2001/XMLSchema" type="xs:string" style="query" name="poi"/>
                    <param xmlns:xs="http://www.w3.org/2001/XMLSchema" type="xs:string" style="query" name="clat"/>
                    <param xmlns:xs="http://www.w3.org/2001/XMLSchema" type="xs:string" style="query" name="clon"/>
                    <param xmlns:xs="http://www.w3.org/2001/XMLSchema" type="xs:string" style="query" name="lat"/>
                    <param xmlns:xs="http://www.w3.org/2001/XMLSchema" type="xs:string" style="query" name="lon"/>
                    <param xmlns:xs="http://www.w3.org/2001/XMLSchema" type="xs:string" style="query" name="elat"/>
                    <param xmlns:xs="http://www.w3.org/2001/XMLSchema" type="xs:string" style="query" name="elon"/>
                    <param xmlns:xs="http://www.w3.org/2001/XMLSchema" type="xs:string" style="query" name="radius"/>
                    <param xmlns:xs="http://www.w3.org/2001/XMLSchema" type="xs:string" style="query" name="zoom"/>
                    <param xmlns:xs="http://www.w3.org/2001/XMLSchema" type="xs:string" style="query" name="north"/>
                    <param xmlns:xs="http://www.w3.org/2001/XMLSchema" type="xs:string" style="query" name="south"/>
                    <param xmlns:xs="http://www.w3.org/2001/XMLSchema" type="xs:string" style="query" name="east"/>
                    <param xmlns:xs="http://www.w3.org/2001/XMLSchema" type="xs:string" style="query" name="west"/>
                    <param xmlns:xs="http://www.w3.org/2001/XMLSchema" type="xs:string" style="query" name="tx"/>
                    <param xmlns:xs="http://www.w3.org/2001/XMLSchema" type="xs:string" style="query" name="ty"/>
                    <param xmlns:xs="http://www.w3.org/2001/XMLSchema" type="xs:string" style="query" name="tz"/>
                    <param xmlns:xs="http://www.w3.org/2001/XMLSchema" type="xs:string" style="query" name="locale"/>
                    <param xmlns:xs="http://www.w3.org/2001/XMLSchema" type="xs:string" style="query" name="proj"/>
                    <param xmlns:xs="http://www.w3.org/2001/XMLSchema" type="xs:string" style="query" name="rotation"/>
                    <param xmlns:xs="http://www.w3.org/2001/XMLSchema" type="xs:string" style="query" name="imw"/>
                    <param xmlns:xs="http://www.w3.org/2001/XMLSchema" type="xs:string" style="query" name="imh"/>
                    <param xmlns:xs="http://www.w3.org/2001/XMLSchema" type="xs:string" style="query" name="imf"/>
                    <param xmlns:xs="http://www.w3.org/2001/XMLSchema" type="xs:string" style="query" name="ims"/>
                    <param xmlns:xs="http://www.w3.org/2001/XMLSchema" type="xs:string" style="query" name="imi"/>
                    <param xmlns:xs="http://www.w3.org/2001/XMLSchema" type="xs:string" style="query" name="oper"/>
                    <param xmlns:xs="http://www.w3.org/2001/XMLSchema" type="xs:string" style="query" name="cltype"/>
                    <param xmlns:xs="http://www.w3.org/2001/XMLSchema" type="xs:string" style="query" name="cache"/>
                    <param xmlns:xs="http://www.w3.org/2001/XMLSchema" type="xs:string" style="query" name="clid"/>
                    <param xmlns:xs="http://www.w3.org/2001/XMLSchema" type="xs:string" style="query" name="stype"/>
                    <param xmlns:xs="http://www.w3.org/2001/XMLSchema" type="xs:string" style="query" name="feat"/>
                    <param xmlns:xs="http://www.w3.org/2001/XMLSchema" type="xs:string" style="query" name="flags"/>
                    <param xmlns:xs="http://www.w3.org/2001/XMLSchema" type="xs:string" style="query" name="cflags"/>
                    <param xmlns:xs="http://www.w3.org/2001/XMLSchema" type="xs:string" style="query" name="tflags"/>
                    <param xmlns:xs="http://www.w3.org/2001/XMLSchema" type="xs:string" style="query" name="rflags"/>
                    <param xmlns:xs="http://www.w3.org/2001/XMLSchema" type="xs:string" style="query" name="mflags"/>
                    <param xmlns:xs="http://www.w3.org/2001/XMLSchema" type="xs:string" style="query" name="gflags"/>
                    <param xmlns:xs="http://www.w3.org/2001/XMLSchema" type="xs:string" style="query" name="debugflags"/>
                    <param xmlns:xs="http://www.w3.org/2001/XMLSchema" type="xs:string" style="query" name="async"/>
                </request>
                <response>
                    <representation mediaType="application/xml"/>
                    <representation mediaType="image/png"/>
                    <representation mediaType="image/jpeg"/>
                    <representation mediaType="image/gif"/>
                    <representation mediaType="image/jpg"/>
                    <representation mediaType="image/swf"/>
                    <representation mediaType="application/x-shockwave-flash"/>
                </response>
            </method>
        </resource>
        <resource path="/{spot :(?i)spot}">
            <method name="GET" id="getMethod">
                <request>
                    <param xmlns:xs="http://www.w3.org/2001/XMLSchema" type="xs:string" style="query" name="lat"/>
                    <param xmlns:xs="http://www.w3.org/2001/XMLSchema" type="xs:string" style="query" name="lon"/>
                    <param xmlns:xs="http://www.w3.org/2001/XMLSchema" type="xs:string" style="query" name="callback"/>
                    <param xmlns:xs="http://www.w3.org/2001/XMLSchema" type="xs:string" style="query" name="gflags"/>
                    <param xmlns:xs="http://www.w3.org/2001/XMLSchema" type="xs:string" style="query" name="debugflags"/>
                </request>
                <response>
                    <representation mediaType="application/xml; charset=UTF-8"/>
                    <representation mediaType="application/json; charset=UTF-8"/>
                    <representation mediaType="application/x-javascript; charset=UTF-8"/>
                </response>
            </method>
        </resource>
        <resource path="/{onebox :(?i)onebox}">
            <method name="GET" id="getMethod">
                <request>
                    <param xmlns:xs="http://www.w3.org/2001/XMLSchema" type="xs:string" style="query" name="obq"/>
                    <param xmlns:xs="http://www.w3.org/2001/XMLSchema" type="xs:string" style="query" name="callback"/>
                    <param xmlns:xs="http://www.w3.org/2001/XMLSchema" type="xs:double" style="query" name="userLat"/>
                    <param xmlns:xs="http://www.w3.org/2001/XMLSchema" type="xs:double" style="query" name="userLon"/>
                    <param xmlns:xs="http://www.w3.org/2001/XMLSchema" type="xs:int" style="query" name="local_count"/>
                    <param xmlns:xs="http://www.w3.org/2001/XMLSchema" type="xs:string" style="query" name="flags"/>
                    <param xmlns:xs="http://www.w3.org/2001/XMLSchema" type="xs:string" style="query" name="cflags"/>
                    <param xmlns:xs="http://www.w3.org/2001/XMLSchema" type="xs:string" style="query" name="tflags"/>
                    <param xmlns:xs="http://www.w3.org/2001/XMLSchema" type="xs:string" style="query" name="rflags"/>
                    <param xmlns:xs="http://www.w3.org/2001/XMLSchema" type="xs:string" style="query" name="mflags"/>
                    <param xmlns:xs="http://www.w3.org/2001/XMLSchema" type="xs:string" style="query" name="gflags"/>
                    <param xmlns:xs="http://www.w3.org/2001/XMLSchema" type="xs:string" style="query" name="obflags"/>
                    <param xmlns:xs="http://www.w3.org/2001/XMLSchema" type="xs:string" style="query" name="debugflags"/>
                    <param xmlns:xs="http://www.w3.org/2001/XMLSchema" type="xs:string" style="query" name="appid"/>
                    <param xmlns:xs="http://www.w3.org/2001/XMLSchema" type="xs:string" style="query" name="appId"/>
                </request>
                <response>
                    <representation mediaType="application/xml; charset=UTF-8"/>
                    <representation mediaType="application/json; charset=UTF-8"/>
                    <representation mediaType="application/x-javascript; charset=UTF-8"/>
                </response>
            </method>
        </resource>
        <resource path="/{geocode :(?i)geocode}">
            <method name="GET" id="getMethod">
                <request>
                    <param xmlns:xs="http://www.w3.org/2001/XMLSchema" type="xs:string" style="query" name="location"/>
                    <param xmlns:xs="http://www.w3.org/2001/XMLSchema" type="xs:string" style="query" name="name"/>
                    <param xmlns:xs="http://www.w3.org/2001/XMLSchema" type="xs:string" style="query" name="woeid"/>
                    <param xmlns:xs="http://www.w3.org/2001/XMLSchema" type="xs:string" style="query" name="addr"/>
                    <param xmlns:xs="http://www.w3.org/2001/XMLSchema" type="xs:string" style="query" name="csz"/>
                    <param xmlns:xs="http://www.w3.org/2001/XMLSchema" type="xs:string" style="query" name="line3"/>
                    <param xmlns:xs="http://www.w3.org/2001/XMLSchema" type="xs:string" style="query" name="house"/>
                    <param xmlns:xs="http://www.w3.org/2001/XMLSchema" type="xs:string" style="query" name="street"/>
                    <param xmlns:xs="http://www.w3.org/2001/XMLSchema" type="xs:string" style="query" name="unittype"/>
                    <param xmlns:xs="http://www.w3.org/2001/XMLSchema" type="xs:string" style="query" name="unit"/>
                    <param xmlns:xs="http://www.w3.org/2001/XMLSchema" type="xs:string" style="query" name="xstreet"/>
                    <param xmlns:xs="http://www.w3.org/2001/XMLSchema" type="xs:string" style="query" name="postal"/>
                    <param xmlns:xs="http://www.w3.org/2001/XMLSchema" type="xs:string" style="query" name="neighborhood"/>
                    <param xmlns:xs="http://www.w3.org/2001/XMLSchema" type="xs:string" style="query" name="city"/>
                    <param xmlns:xs="http://www.w3.org/2001/XMLSchema" type="xs:string" style="query" name="county"/>
                    <param xmlns:xs="http://www.w3.org/2001/XMLSchema" type="xs:string" style="query" name="state"/>
                    <param xmlns:xs="http://www.w3.org/2001/XMLSchema" type="xs:string" style="query" name="country"/>
                    <param xmlns:xs="http://www.w3.org/2001/XMLSchema" type="xs:string" style="query" name="locale"/>
                    <param xmlns:xs="http://www.w3.org/2001/XMLSchema" type="xs:string" style="query" name=".intl"/>
                    <param xmlns:xs="http://www.w3.org/2001/XMLSchema" type="xs:string" style="query" name="start"/>
                    <param xmlns:xs="http://www.w3.org/2001/XMLSchema" type="xs:string" style="query" name="count"/>
                    <param xmlns:xs="http://www.w3.org/2001/XMLSchema" type="xs:string" style="query" name="offset"/>
                    <param xmlns:xs="http://www.w3.org/2001/XMLSchema" type="xs:string" style="query" name="imw"/>
                    <param xmlns:xs="http://www.w3.org/2001/XMLSchema" type="xs:string" style="query" name="imh"/>
                    <param xmlns:xs="http://www.w3.org/2001/XMLSchema" type="xs:string" style="query" name="imf"/>
                    <param xmlns:xs="http://www.w3.org/2001/XMLSchema" type="xs:string" style="query" name="ims"/>
                    <param xmlns:xs="http://www.w3.org/2001/XMLSchema" type="xs:string" style="query" name="imi"/>
                    <param xmlns:xs="http://www.w3.org/2001/XMLSchema" type="xs:string" style="query" name="cache"/>
                    <param xmlns:xs="http://www.w3.org/2001/XMLSchema" type="xs:string" style="query" name="appid"/>
                    <param xmlns:xs="http://www.w3.org/2001/XMLSchema" type="xs:string" style="query" name="oper"/>
                    <param xmlns:xs="http://www.w3.org/2001/XMLSchema" type="xs:string" style="query" name="cltype"/>
                    <param xmlns:xs="http://www.w3.org/2001/XMLSchema" type="xs:string" style="query" name="clid"/>
                    <param xmlns:xs="http://www.w3.org/2001/XMLSchema" type="xs:string" style="query" name="callback"/>
                    <param xmlns:xs="http://www.w3.org/2001/XMLSchema" type="xs:string" style="query" name="appId"/>
                    <param xmlns:xs="http://www.w3.org/2001/XMLSchema" type="xs:string" style="query" name="flags"/>
                    <param xmlns:xs="http://www.w3.org/2001/XMLSchema" type="xs:string" style="query" name="cflags"/>
                    <param xmlns:xs="http://www.w3.org/2001/XMLSchema" type="xs:string" style="query" name="tflags"/>
                    <param xmlns:xs="http://www.w3.org/2001/XMLSchema" type="xs:string" style="query" name="rflags"/>
                    <param xmlns:xs="http://www.w3.org/2001/XMLSchema" type="xs:string" style="query" name="mflags"/>
                    <param xmlns:xs="http://www.w3.org/2001/XMLSchema" type="xs:string" style="query" name="gflags"/>
                    <param xmlns:xs="http://www.w3.org/2001/XMLSchema" type="xs:string" style="query" name="debugflags"/>
                </request>
                <response>
                    <representation mediaType="application/xml; charset=UTF-8"/>
                    <representation mediaType="application/json; charset=UTF-8"/>
                    <representation mediaType="application/x-javascript; charset=UTF-8"/>
                </response>
            </method>
        </resource>
        <resource path="/{traffic :(?i)traffic}">
            <method name="GET" id="getMethod">
                <request>
                    <param xmlns:xs="http://www.w3.org/2001/XMLSchema" type="xs:string" style="query" name="q"/>
                    <param xmlns:xs="http://www.w3.org/2001/XMLSchema" type="xs:string" style="query" name="clat"/>
                    <param xmlns:xs="http://www.w3.org/2001/XMLSchema" type="xs:string" style="query" name="clon"/>
                    <param xmlns:xs="http://www.w3.org/2001/XMLSchema" type="xs:string" style="query" name="lat"/>
                    <param xmlns:xs="http://www.w3.org/2001/XMLSchema" type="xs:string" style="query" name="lon"/>
                    <param xmlns:xs="http://www.w3.org/2001/XMLSchema" type="xs:string" style="query" name="location"/>
                    <param xmlns:xs="http://www.w3.org/2001/XMLSchema" type="xs:string" style="query" name="name"/>
                    <param xmlns:xs="http://www.w3.org/2001/XMLSchema" type="xs:string" style="query" name="woeid"/>
                    <param xmlns:xs="http://www.w3.org/2001/XMLSchema" type="xs:string" style="query" name="addr"/>
                    <param xmlns:xs="http://www.w3.org/2001/XMLSchema" type="xs:string" style="query" name="csz"/>
                    <param xmlns:xs="http://www.w3.org/2001/XMLSchema" type="xs:string" style="query" name="line3"/>
                    <param xmlns:xs="http://www.w3.org/2001/XMLSchema" type="xs:string" style="query" name="house"/>
                    <param xmlns:xs="http://www.w3.org/2001/XMLSchema" type="xs:string" style="query" name="street"/>
                    <param xmlns:xs="http://www.w3.org/2001/XMLSchema" type="xs:string" style="query" name="unittype"/>
                    <param xmlns:xs="http://www.w3.org/2001/XMLSchema" type="xs:string" style="query" name="unit"/>
                    <param xmlns:xs="http://www.w3.org/2001/XMLSchema" type="xs:string" style="query" name="xstreet"/>
                    <param xmlns:xs="http://www.w3.org/2001/XMLSchema" type="xs:string" style="query" name="postal"/>
                    <param xmlns:xs="http://www.w3.org/2001/XMLSchema" type="xs:string" style="query" name="neighborhood"/>
                    <param xmlns:xs="http://www.w3.org/2001/XMLSchema" type="xs:string" style="query" name="city"/>
                    <param xmlns:xs="http://www.w3.org/2001/XMLSchema" type="xs:string" style="query" name="county"/>
                    <param xmlns:xs="http://www.w3.org/2001/XMLSchema" type="xs:string" style="query" name="state"/>
                    <param xmlns:xs="http://www.w3.org/2001/XMLSchema" type="xs:string" style="query" name="country"/>
                    <param xmlns:xs="http://www.w3.org/2001/XMLSchema" default="10000" type="xs:string" style="query" name="radius"/>
                    <param xmlns:xs="http://www.w3.org/2001/XMLSchema" default="0" type="xs:string" style="query" name="minsp"/>
                    <param xmlns:xs="http://www.w3.org/2001/XMLSchema" default="200" type="xs:string" style="query" name="maxsp"/>
                    <param xmlns:xs="http://www.w3.org/2001/XMLSchema" type="xs:string" style="query" name="sp1"/>
                    <param xmlns:xs="http://www.w3.org/2001/XMLSchema" type="xs:string" style="query" name="sp2"/>
                    <param xmlns:xs="http://www.w3.org/2001/XMLSchema" type="xs:string" style="query" name="sp3"/>
                    <param xmlns:xs="http://www.w3.org/2001/XMLSchema" default="1" type="xs:string" style="query" name="minsev"/>
                    <param xmlns:xs="http://www.w3.org/2001/XMLSchema" default="1" type="xs:string" style="query" name="maxsev"/>
                    <param xmlns:xs="http://www.w3.org/2001/XMLSchema" type="xs:string" style="query" name="mintime"/>
                    <param xmlns:xs="http://www.w3.org/2001/XMLSchema" type="xs:string" style="query" name="maxtime"/>
                    <param xmlns:xs="http://www.w3.org/2001/XMLSchema" type="xs:string" style="query" name="t"/>
                    <param xmlns:xs="http://www.w3.org/2001/XMLSchema" type="xs:string" style="query" name="locale"/>
                    <param xmlns:xs="http://www.w3.org/2001/XMLSchema" type="xs:string" style="query" name=".intl"/>
                    <param xmlns:xs="http://www.w3.org/2001/XMLSchema" type="xs:string" style="query" name="sfmt"/>
                    <param xmlns:xs="http://www.w3.org/2001/XMLSchema" type="xs:string" style="query" name="level"/>
                    <param xmlns:xs="http://www.w3.org/2001/XMLSchema" type="xs:string" style="query" name="imw"/>
                    <param xmlns:xs="http://www.w3.org/2001/XMLSchema" type="xs:string" style="query" name="imh"/>
                    <param xmlns:xs="http://www.w3.org/2001/XMLSchema" type="xs:string" style="query" name="callback"/>
                    <param xmlns:xs="http://www.w3.org/2001/XMLSchema" type="xs:string" style="query" name="cache"/>
                    <param xmlns:xs="http://www.w3.org/2001/XMLSchema" type="xs:string" style="query" name="flags"/>
                    <param xmlns:xs="http://www.w3.org/2001/XMLSchema" type="xs:string" style="query" name="cflags"/>
                    <param xmlns:xs="http://www.w3.org/2001/XMLSchema" type="xs:string" style="query" name="tflags"/>
                    <param xmlns:xs="http://www.w3.org/2001/XMLSchema" type="xs:string" style="query" name="rflags"/>
                    <param xmlns:xs="http://www.w3.org/2001/XMLSchema" type="xs:string" style="query" name="mflags"/>
                    <param xmlns:xs="http://www.w3.org/2001/XMLSchema" type="xs:string" style="query" name="gflags"/>
                    <param xmlns:xs="http://www.w3.org/2001/XMLSchema" type="xs:string" style="query" name="debugflags"/>
                </request>
                <response>
                    <representation mediaType="application/xml; charset=UTF-8"/>
                    <representation mediaType="application/json; charset=UTF-8"/>
                    <representation mediaType="application/x-javascript; charset=UTF-8"/>
                </response>
            </method>
        </resource>
        <resource path="/{directions :(?i)directions}">
            <method name="GET" id="getMethod">
                <request>
                    <param xmlns:xs="http://www.w3.org/2001/XMLSchema" type="xs:string" style="query" name="oq"/>
                    <param xmlns:xs="http://www.w3.org/2001/XMLSchema" type="xs:string" style="query" name="dq"/>
                    <param xmlns:xs="http://www.w3.org/2001/XMLSchema" type="xs:string" style="query" name="routeid"/>
                    <param xmlns:xs="http://www.w3.org/2001/XMLSchema" type="xs:string" style="query" name="w1q"/>
                    <param xmlns:xs="http://www.w3.org/2001/XMLSchema" type="xs:string" style="query" name="w2q"/>
                    <param xmlns:xs="http://www.w3.org/2001/XMLSchema" type="xs:string" style="query" name="w3q"/>
                    <param xmlns:xs="http://www.w3.org/2001/XMLSchema" type="xs:string" style="query" name="w4q"/>
                    <param xmlns:xs="http://www.w3.org/2001/XMLSchema" type="xs:string" style="query" name="w5q"/>
                    <param xmlns:xs="http://www.w3.org/2001/XMLSchema" type="xs:string" style="query" name="okey"/>
                    <param xmlns:xs="http://www.w3.org/2001/XMLSchema" type="xs:string" style="query" name="oquality"/>
                    <param xmlns:xs="http://www.w3.org/2001/XMLSchema" type="xs:string" style="query" name="dkey"/>
                    <param xmlns:xs="http://www.w3.org/2001/XMLSchema" type="xs:string" style="query" name="dquality"/>
                    <param xmlns:xs="http://www.w3.org/2001/XMLSchema" type="xs:string" style="query" name="olat"/>
                    <param xmlns:xs="http://www.w3.org/2001/XMLSchema" type="xs:string" style="query" name="olon"/>
                    <param xmlns:xs="http://www.w3.org/2001/XMLSchema" type="xs:string" style="query" name="ocount"/>
                    <param xmlns:xs="http://www.w3.org/2001/XMLSchema" type="xs:string" style="query" name="dlat"/>
                    <param xmlns:xs="http://www.w3.org/2001/XMLSchema" type="xs:string" style="query" name="dlon"/>
                    <param xmlns:xs="http://www.w3.org/2001/XMLSchema" type="xs:string" style="query" name="dcount"/>
                    <param xmlns:xs="http://www.w3.org/2001/XMLSchema" type="xs:string" style="query" name="w1key"/>
                    <param xmlns:xs="http://www.w3.org/2001/XMLSchema" type="xs:string" style="query" name="w1lat"/>
                    <param xmlns:xs="http://www.w3.org/2001/XMLSchema" type="xs:string" style="query" name="w1lon"/>
                    <param xmlns:xs="http://www.w3.org/2001/XMLSchema" type="xs:string" style="query" name="w1radius"/>
                    <param xmlns:xs="http://www.w3.org/2001/XMLSchema" type="xs:string" style="query" name="w1north"/>
                    <param xmlns:xs="http://www.w3.org/2001/XMLSchema" type="xs:string" style="query" name="w1south"/>
                    <param xmlns:xs="http://www.w3.org/2001/XMLSchema" type="xs:string" style="query" name="w1east"/>
                    <param xmlns:xs="http://www.w3.org/2001/XMLSchema" type="xs:string" style="query" name="w1west"/>
                    <param xmlns:xs="http://www.w3.org/2001/XMLSchema" type="xs:string" style="query" name="w1count"/>
                    <param xmlns:xs="http://www.w3.org/2001/XMLSchema" type="xs:string" style="query" name="w1flags"/>
                    <param xmlns:xs="http://www.w3.org/2001/XMLSchema" type="xs:string" style="query" name="mode"/>
                    <param xmlns:xs="http://www.w3.org/2001/XMLSchema" type="xs:string" style="query" name="tmode"/>
                    <param xmlns:xs="http://www.w3.org/2001/XMLSchema" type="xs:string" style="query" name="tthresa"/>
                    <param xmlns:xs="http://www.w3.org/2001/XMLSchema" type="xs:string" style="query" name="tthresp"/>
                    <param xmlns:xs="http://www.w3.org/2001/XMLSchema" type="xs:string" style="query" name="time"/>
                    <param xmlns:xs="http://www.w3.org/2001/XMLSchema" type="xs:string" style="query" name="snap"/>
                    <param xmlns:xs="http://www.w3.org/2001/XMLSchema" type="xs:string" style="query" name="north"/>
                    <param xmlns:xs="http://www.w3.org/2001/XMLSchema" type="xs:string" style="query" name="south"/>
                    <param xmlns:xs="http://www.w3.org/2001/XMLSchema" type="xs:string" style="query" name="east"/>
                    <param xmlns:xs="http://www.w3.org/2001/XMLSchema" type="xs:string" style="query" name="west"/>
                    <param xmlns:xs="http://www.w3.org/2001/XMLSchema" type="xs:string" style="query" name="gfmt"/>
                    <param xmlns:xs="http://www.w3.org/2001/XMLSchema" type="xs:string" style="query" name="gep"/>
                    <param xmlns:xs="http://www.w3.org/2001/XMLSchema" type="xs:string" style="query" name="ver"/>
                    <param xmlns:xs="http://www.w3.org/2001/XMLSchema" type="xs:string" style="query" name="fit"/>
                    <param xmlns:xs="http://www.w3.org/2001/XMLSchema" type="xs:string" style="query" name="row"/>
                    <param xmlns:xs="http://www.w3.org/2001/XMLSchema" type="xs:string" style="query" name="col"/>
                    <param xmlns:xs="http://www.w3.org/2001/XMLSchema" type="xs:string" style="query" name="nrows"/>
                    <param xmlns:xs="http://www.w3.org/2001/XMLSchema" type="xs:string" style="query" name="ncols"/>
                    <param xmlns:xs="http://www.w3.org/2001/XMLSchema" type="xs:string" style="query" name="tl"/>
                    <param xmlns:xs="http://www.w3.org/2001/XMLSchema" type="xs:string" style="query" name="r"/>
                    <param xmlns:xs="http://www.w3.org/2001/XMLSchema" type="xs:string" style="query" name="tw"/>
                    <param xmlns:xs="http://www.w3.org/2001/XMLSchema" type="xs:string" style="query" name="th"/>
                    <param xmlns:xs="http://www.w3.org/2001/XMLSchema" type="xs:string" style="query" name="tpts"/>
                    <param xmlns:xs="http://www.w3.org/2001/XMLSchema" type="xs:string" style="query" name="callback"/>
                    <param xmlns:xs="http://www.w3.org/2001/XMLSchema" type="xs:string" style="query" name="cache"/>
                    <param xmlns:xs="http://www.w3.org/2001/XMLSchema" type="xs:string" style="query" name="flags"/>
                    <param xmlns:xs="http://www.w3.org/2001/XMLSchema" type="xs:string" style="query" name="cflags"/>
                    <param xmlns:xs="http://www.w3.org/2001/XMLSchema" type="xs:string" style="query" name="tflags"/>
                    <param xmlns:xs="http://www.w3.org/2001/XMLSchema" type="xs:string" style="query" name="rflags"/>
                    <param xmlns:xs="http://www.w3.org/2001/XMLSchema" type="xs:string" style="query" name="mflags"/>
                    <param xmlns:xs="http://www.w3.org/2001/XMLSchema" type="xs:string" style="query" name="gflags"/>
                    <param xmlns:xs="http://www.w3.org/2001/XMLSchema" type="xs:string" style="query" name="debugflags"/>
                </request>
                <response>
                    <representation mediaType="application/xml; charset=UTF-8"/>
                    <representation mediaType="application/json; charset=UTF-8"/>
                    <representation mediaType="application/x-javascript; charset=UTF-8"/>
                </response>
            </method>
        </resource>
        <resource path="/{venue :(?i)venue}">
            <resource path="lookup">
                <method name="GET" id="getMethod">
                    <request>
                        <param xmlns:xs="http://www.w3.org/2001/XMLSchema" type="xs:string" style="query" name="callback"/>
                        <param xmlns:xs="http://www.w3.org/2001/XMLSchema" type="xs:string" style="query" name="vlflags"/>
                        <param xmlns:xs="http://www.w3.org/2001/XMLSchema" type="xs:string" style="query" name="debugflags"/>
                    </request>
                    <response>
                        <representation mediaType="application/xml; charset=UTF-8"/>
                        <representation mediaType="application/json; charset=UTF-8"/>
                        <representation mediaType="application/x-javascript; charset=UTF-8"/>
                    </response>
                </method>
            </resource>
            <resource path="digest">
                <method name="GET" id="getMethod">
                    <request>
                        <param xmlns:xs="http://www.w3.org/2001/XMLSchema" type="xs:string" style="query" name="callback"/>
                        <param xmlns:xs="http://www.w3.org/2001/XMLSchema" type="xs:string" style="query" name="vsflags"/>
                        <param xmlns:xs="http://www.w3.org/2001/XMLSchema" type="xs:string" style="query" name="debugflags"/>
                    </request>
                    <response>
                        <representation mediaType="application/xml; charset=UTF-8"/>
                        <representation mediaType="application/json; charset=UTF-8"/>
                        <representation mediaType="application/x-javascript; charset=UTF-8"/>
                    </response>
                </method>
            </resource>
            <resource path="search">
                <method name="GET" id="getMethod">
                    <request>
                        <param xmlns:xs="http://www.w3.org/2001/XMLSchema" type="xs:string" style="query" name="callback"/>
                        <param xmlns:xs="http://www.w3.org/2001/XMLSchema" type="xs:string" style="query" name="vsflags"/>
                        <param xmlns:xs="http://www.w3.org/2001/XMLSchema" type="xs:string" style="query" name="debugflags"/>
                    </request>
                    <response>
                        <representation mediaType="application/xml; charset=UTF-8"/>
                        <representation mediaType="application/json; charset=UTF-8"/>
                        <representation mediaType="application/x-javascript; charset=UTF-8"/>
                    </response>
                </method>
            </resource>
        </resource>
        <resource path="/{deviation :(?i)deviation}">
            <method name="GET" id="getMethod">
                <request>
                    <param xmlns:xs="http://www.w3.org/2001/XMLSchema" type="xs:string" style="query" name="cache"/>
                    <param xmlns:xs="http://www.w3.org/2001/XMLSchema" type="xs:string" style="query" name="callback"/>
                    <param xmlns:xs="http://www.w3.org/2001/XMLSchema" type="xs:string" style="query" name="key"/>
                    <param xmlns:xs="http://www.w3.org/2001/XMLSchema" type="xs:string" style="query" name="value"/>
                    <param xmlns:xs="http://www.w3.org/2001/XMLSchema" type="xs:string" style="query" name="file"/>
                    <param xmlns:xs="http://www.w3.org/2001/XMLSchema" type="xs:string" style="query" name="action"/>
                    <param xmlns:xs="http://www.w3.org/2001/XMLSchema" type="xs:string" style="query" name="comment"/>
                    <param xmlns:xs="http://www.w3.org/2001/XMLSchema" type="xs:string" style="query" name="debugflags"/>
                </request>
                <response>
                    <representation mediaType="application/xml"/>
                    <representation mediaType="application/json"/>
                    <representation mediaType="application/x-javascript"/>
                </response>
            </method>
        </resource>
        <resource path="/{tile :(?i)tile}">
            <resource path="version">
                <method name="GET" id="getMethod">
                    <request>
                        <param xmlns:xs="http://www.w3.org/2001/XMLSchema" type="xs:string" style="query" name="cache"/>
                        <param xmlns:xs="http://www.w3.org/2001/XMLSchema" type="xs:string" style="query" name="callback"/>
                        <param xmlns:xs="http://www.w3.org/2001/XMLSchema" type="xs:string" style="query" name="appid"/>
                        <param xmlns:xs="http://www.w3.org/2001/XMLSchema" type="xs:string" style="query" name="debugflags"/>
                    </request>
                    <response>
                        <representation mediaType="application/xml"/>
                        <representation mediaType="application/json"/>
                        <representation mediaType="application/x-javascript"/>
                    </response>
                </method>
            </resource>
            <resource path="copyright">
                <method name="GET" id="getMethod">
                    <request>
                        <param xmlns:xs="http://www.w3.org/2001/XMLSchema" type="xs:string" style="query" name="clat"/>
                        <param xmlns:xs="http://www.w3.org/2001/XMLSchema" default="1.0" type="xs:string" style="query" name="clon"/>
                        <param xmlns:xs="http://www.w3.org/2001/XMLSchema" type="xs:string" style="query" name="lat"/>
                        <param xmlns:xs="http://www.w3.org/2001/XMLSchema" type="xs:string" style="query" name="lon"/>
                        <param xmlns:xs="http://www.w3.org/2001/XMLSchema" type="xs:string" style="query" name="v"/>
                        <param xmlns:xs="http://www.w3.org/2001/XMLSchema" type="xs:string" style="query" name="x"/>
                        <param xmlns:xs="http://www.w3.org/2001/XMLSchema" type="xs:string" style="query" name="y"/>
                        <param xmlns:xs="http://www.w3.org/2001/XMLSchema" type="xs:string" style="query" name="z"/>
                        <param xmlns:xs="http://www.w3.org/2001/XMLSchema" type="xs:string" style="query" name="ns"/>
                        <param xmlns:xs="http://www.w3.org/2001/XMLSchema" type="xs:string" style="query" name="appid"/>
                        <param xmlns:xs="http://www.w3.org/2001/XMLSchema" type="xs:string" style="query" name="ew"/>
                        <param xmlns:xs="http://www.w3.org/2001/XMLSchema" type="xs:string" style="query" name="top"/>
                        <param xmlns:xs="http://www.w3.org/2001/XMLSchema" type="xs:string" style="query" name="left"/>
                        <param xmlns:xs="http://www.w3.org/2001/XMLSchema" type="xs:string" style="query" name="r"/>
                        <param xmlns:xs="http://www.w3.org/2001/XMLSchema" type="xs:string" style="query" name="t"/>
                        <param xmlns:xs="http://www.w3.org/2001/XMLSchema" type="xs:string" style="query" name="cache"/>
                        <param xmlns:xs="http://www.w3.org/2001/XMLSchema" type="xs:string" style="query" name="callback"/>
                        <param xmlns:xs="http://www.w3.org/2001/XMLSchema" type="xs:string" style="query" name="debugflags"/>
                    </request>
                    <response>
                        <representation mediaType="application/xml"/>
                        <representation mediaType="application/json"/>
                        <representation mediaType="application/x-javascript"/>
                    </response>
                </method>
            </resource>
        </resource>
        <resource path="/{inhousedata :(?i)inhousedata}">
            <method name="GET" id="getMethod">
                <request>
                    <param xmlns:xs="http://www.w3.org/2001/XMLSchema" type="xs:string" style="query" name="callback"/>
                </request>
                <response>
                    <representation mediaType="application/xml"/>
                    <representation mediaType="application/json"/>
                    <representation mediaType="application/x-javascript"/>
                </response>
            </method>
        </resource>
        <resource path="/{contentingestion :(?i)contentingestion}">
            <method name="GET" id="getMethod">
                <request>
                    <param xmlns:xs="http://www.w3.org/2001/XMLSchema" type="xs:string" style="query" name="callback"/>
                    <param xmlns:xs="http://www.w3.org/2001/XMLSchema" type="xs:string" style="query" name="appId"/>
                    <param xmlns:xs="http://www.w3.org/2001/XMLSchema" type="xs:string" style="query" name="appid"/>
                    <param xmlns:xs="http://www.w3.org/2001/XMLSchema" type="xs:string" style="query" name="debugflags"/>
                </request>
                <response>
                    <representation mediaType="application/xml; charset=UTF-8"/>
                    <representation mediaType="application/json; charset=UTF-8"/>
                    <representation mediaType="application/x-javascript; charset=UTF-8"/>
                </response>
            </method>
        </resource>
        <resource path="/{namedplace :(?i)namedplace}">
            <method name="GET" id="getMethod">
                <request>
                    <param xmlns:xs="http://www.w3.org/2001/XMLSchema" type="xs:string" style="query" name="q"/>
                    <param xmlns:xs="http://www.w3.org/2001/XMLSchema" type="xs:string" style="query" name="callback"/>
                    <param xmlns:xs="http://www.w3.org/2001/XMLSchema" type="xs:string" style="query" name="gflags"/>
                    <param xmlns:xs="http://www.w3.org/2001/XMLSchema" type="xs:string" style="query" name="debugflags"/>
                    <param xmlns:xs="http://www.w3.org/2001/XMLSchema" type="xs:string" style="query" name="appid"/>
                    <param xmlns:xs="http://www.w3.org/2001/XMLSchema" type="xs:string" style="query" name="appId"/>
                </request>
                <response>
                    <representation mediaType="application/xml; charset=UTF-8"/>
                    <representation mediaType="application/json; charset=UTF-8"/>
                    <representation mediaType="application/x-javascript; charset=UTF-8"/>
                </response>
            </method>
        </resource>
        <resource path="/{whereami :(?i)whereami}">
            <resource path="search">
                <method name="GET" id="getMethod">
                    <request>
                        <param xmlns:xs="http://www.w3.org/2001/XMLSchema" type="xs:string" style="query" name="callback"/>
                        <param xmlns:xs="http://www.w3.org/2001/XMLSchema" type="xs:string" style="query" name="debugflags"/>
                    </request>
                    <response>
                        <representation mediaType="application/xml; charset=UTF-8"/>
                        <representation mediaType="application/json; charset=UTF-8"/>
                        <representation mediaType="application/x-javascript; charset=UTF-8"/>
                    </response>
                </method>
            </resource>
            <resource path="lookup">
                <method name="GET" id="getMethod">
                    <request>
                        <param xmlns:xs="http://www.w3.org/2001/XMLSchema" type="xs:string" style="query" name="callback"/>
                        <param xmlns:xs="http://www.w3.org/2001/XMLSchema" type="xs:string" style="query" name="debugflags"/>
                    </request>
                    <response>
                        <representation mediaType="application/xml; charset=UTF-8"/>
                        <representation mediaType="application/json; charset=UTF-8"/>
                        <representation mediaType="application/x-javascript; charset=UTF-8"/>
                    </response>
                </method>
            </resource>
        </resource>
        <resource path="/{findlocation :(?i)findlocation}">
            <method name="GET" id="getMethod">
                <request>
                    <param xmlns:xs="http://www.w3.org/2001/XMLSchema" type="xs:string" style="query" name="location"/>
                    <param xmlns:xs="http://www.w3.org/2001/XMLSchema" type="xs:string" style="query" name="name"/>
                    <param xmlns:xs="http://www.w3.org/2001/XMLSchema" type="xs:string" style="query" name="woeid"/>
                    <param xmlns:xs="http://www.w3.org/2001/XMLSchema" type="xs:string" style="query" name="addr"/>
                    <param xmlns:xs="http://www.w3.org/2001/XMLSchema" type="xs:string" style="query" name="csz"/>
                    <param xmlns:xs="http://www.w3.org/2001/XMLSchema" type="xs:string" style="query" name="line3"/>
                    <param xmlns:xs="http://www.w3.org/2001/XMLSchema" type="xs:string" style="query" name="house"/>
                    <param xmlns:xs="http://www.w3.org/2001/XMLSchema" type="xs:string" style="query" name="street"/>
                    <param xmlns:xs="http://www.w3.org/2001/XMLSchema" type="xs:string" style="query" name="unittype"/>
                    <param xmlns:xs="http://www.w3.org/2001/XMLSchema" type="xs:string" style="query" name="unit"/>
                    <param xmlns:xs="http://www.w3.org/2001/XMLSchema" type="xs:string" style="query" name="xstreet"/>
                    <param xmlns:xs="http://www.w3.org/2001/XMLSchema" type="xs:string" style="query" name="postal"/>
                    <param xmlns:xs="http://www.w3.org/2001/XMLSchema" type="xs:string" style="query" name="neighborhood"/>
                    <param xmlns:xs="http://www.w3.org/2001/XMLSchema" type="xs:string" style="query" name="city"/>
                    <param xmlns:xs="http://www.w3.org/2001/XMLSchema" type="xs:string" style="query" name="county"/>
                    <param xmlns:xs="http://www.w3.org/2001/XMLSchema" type="xs:string" style="query" name="state"/>
                    <param xmlns:xs="http://www.w3.org/2001/XMLSchema" type="xs:string" style="query" name="country"/>
                    <param xmlns:xs="http://www.w3.org/2001/XMLSchema" type="xs:string" style="query" name="locale"/>
                    <param xmlns:xs="http://www.w3.org/2001/XMLSchema" type="xs:string" style="query" name=".intl"/>
                    <param xmlns:xs="http://www.w3.org/2001/XMLSchema" type="xs:string" style="query" name="start"/>
                    <param xmlns:xs="http://www.w3.org/2001/XMLSchema" type="xs:string" style="query" name="count"/>
                    <param xmlns:xs="http://www.w3.org/2001/XMLSchema" type="xs:string" style="query" name="offset"/>
                    <param xmlns:xs="http://www.w3.org/2001/XMLSchema" type="xs:string" style="query" name="imw"/>
                    <param xmlns:xs="http://www.w3.org/2001/XMLSchema" type="xs:string" style="query" name="imh"/>
                    <param xmlns:xs="http://www.w3.org/2001/XMLSchema" type="xs:string" style="query" name="imf"/>
                    <param xmlns:xs="http://www.w3.org/2001/XMLSchema" type="xs:string" style="query" name="ims"/>
                    <param xmlns:xs="http://www.w3.org/2001/XMLSchema" type="xs:string" style="query" name="imi"/>
                    <param xmlns:xs="http://www.w3.org/2001/XMLSchema" type="xs:string" style="query" name="cache"/>
                    <param xmlns:xs="http://www.w3.org/2001/XMLSchema" type="xs:string" style="query" name="appid"/>
                    <param xmlns:xs="http://www.w3.org/2001/XMLSchema" type="xs:string" style="query" name="oper"/>
                    <param xmlns:xs="http://www.w3.org/2001/XMLSchema" type="xs:string" style="query" name="cltype"/>
                    <param xmlns:xs="http://www.w3.org/2001/XMLSchema" type="xs:string" style="query" name="clid"/>
                    <param xmlns:xs="http://www.w3.org/2001/XMLSchema" type="xs:string" style="query" name="callback"/>
                    <param xmlns:xs="http://www.w3.org/2001/XMLSchema" type="xs:string" style="query" name="appId"/>
                    <param xmlns:xs="http://www.w3.org/2001/XMLSchema" type="xs:string" style="query" name="flags"/>
                    <param xmlns:xs="http://www.w3.org/2001/XMLSchema" type="xs:string" style="query" name="cflags"/>
                    <param xmlns:xs="http://www.w3.org/2001/XMLSchema" type="xs:string" style="query" name="tflags"/>
                    <param xmlns:xs="http://www.w3.org/2001/XMLSchema" type="xs:string" style="query" name="rflags"/>
                    <param xmlns:xs="http://www.w3.org/2001/XMLSchema" type="xs:string" style="query" name="mflags"/>
                    <param xmlns:xs="http://www.w3.org/2001/XMLSchema" type="xs:string" style="query" name="gflags"/>
                    <param xmlns:xs="http://www.w3.org/2001/XMLSchema" type="xs:string" style="query" name="debugflags"/>
                </request>
                <response>
                    <representation mediaType="application/xml; charset=UTF-8"/>
                    <representation mediaType="application/json; charset=UTF-8"/>
                    <representation mediaType="application/x-javascript; charset=UTF-8"/>
                </response>
            </method>
        </resource>
    </resources>
</application>
"""  # noqa


def test_request_amount():
    wh = WADLHandler(WADL_SAMPLE)
    assert len(wh.requests) == 19


def test_param_url():
    wh = WADLHandler(WADL_SAMPLE)
    req = wh.requests

    assert req[0].location == "https://some.sub.example.com/stats/{jobId}"
    assert req[1].location == "https://some.sub.example.com/summary/{jobId}"
    assert req[2].location == "https://some.sub.example.com/spot"
    assert req[3].location == "https://some.sub.example.com/onebox"
    assert req[4].location == "https://some.sub.example.com/geocode"
    assert req[5].location == "https://some.sub.example.com/traffic"
    assert req[6].location == "https://some.sub.example.com/directions"
    assert req[7].location == "https://some.sub.example.com/venue/lookup"
    assert req[8].location == "https://some.sub.example.com/venue/digest"
    assert req[9].location == "https://some.sub.example.com/venue/search"
    assert req[10].location == "https://some.sub.example.com/deviation"
    assert req[11].location == "https://some.sub.example.com/tile/version"
    assert req[12].location == "https://some.sub.example.com/tile/copyright"
    assert req[13].location == "https://some.sub.example.com/inhousedata"
    assert req[14].location == "https://some.sub.example.com/contentingestion"
    assert req[15].location == "https://some.sub.example.com/namedplace"
    assert req[16].location == "https://some.sub.example.com/whereami/search"
    assert req[17].location == "https://some.sub.example.com/whereami/lookup"
    assert req[18].location == "https://some.sub.example.com/findlocation"


@responses.activate
def test_set_value_param_url():
    jobId = 123
    responses.add(
        responses.GET,
        "https://some.sub.example.com/stats/{}".format(jobId),
        status=200,
    )
    responses.add(
        responses.GET,
        "https://some.sub.example.com/summary/{}".format(jobId),
        status=200,
    )

    runner = CliRunner()
    with runner.isolated_filesystem():
        with open("test_param_url.wadl", "w") as f:
            f.write(WADL_SAMPLE)

        runner.invoke(wadalize, ["-p", "jobId:{}".format(jobId), "test_param_url.wadl"])

        req = responses.calls
        assert (
            str(req[0].request.url)
            == "https://some.sub.example.com/stats/123?q=&poi=&clat=&clon=&lat=&lon=&elat=&elon=&radius=&zoom=&north=&south=&east=&west=&tx=&ty=&tz=&locale=&proj=&rotation=&imw=&imh=&imf=&ims=&imi=&oper=&cltype=&cache=&clid=&stype=&feat=&flags=&cflags=&tflags=&rflags=&mflags=&gflags=&debugflags=&async="  # noqa E501
        )
        assert (
            str(req[1].request.url)
            == "https://some.sub.example.com/summary/123?q=&poi=&clat=&clon=&lat=&lon=&elat=&elon=&radius=&zoom=&north=&south=&east=&west=&tx=&ty=&tz=&locale=&proj=&rotation=&imw=&imh=&imf=&ims=&imi=&oper=&cltype=&cache=&clid=&stype=&feat=&flags=&cflags=&tflags=&rflags=&mflags=&gflags=&debugflags=&async="  # noqa E501
        )
