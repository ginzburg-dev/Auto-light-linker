####################################################################
#
# Copyright (c) 2023, Dmitri Ginzburg.  All Rights Reserved.
#
####################################################################

import time
import re
from maya import cmds
import maya.api.OpenMaya as om
import maya.app.renderSetup.model.override as override
import maya.app.renderSetup.model.selector as selector
import maya.app.renderSetup.model.collection as collection
import maya.app.renderSetup.model.renderLayer as renderLayer
import maya.app.renderSetup.model.renderSetup as renderSetup
import maya.app.renderSetup.model.utils as utils

def getSelection():
    cmds.select(hierarchy = True)
    activelayer = cmds.ls(sl = True, typ='shape', long=True)
    return activelayer;

def getInvertSelection(selection):
    allObj = cmds.ls(typ='shape', long=True)
    invertShapes = []
    for i in allObj:
        chk = 0;
        for k in selection:
            if i == k:
                chk = 1;
        if chk == 0:
        invertShapes.append(i);
    return invertShapes;

def isRSLight(shapename):
    check = 1;
    try:
        cmds.getAttr(shapename+'.exposure');
    except:
        check = 0;
    return check;

def getShapeName(longName):
    spliti = longName.split('|');
    result = spliti[len(spliti)-1];
    return result;

def getLongName(shortList):
    lightsAll = getAllRSLights('long');
    list_result = []
    for i in shortList:
        for k in lightsAll:
            if i == getShapeName(k):
                list_result.append(k);
    return list_result;

def getAllRSLights(formats):
    lightsRS = [];
    sel = [];
    if formats == 'long':
        sel = cmds.ls(long=True, typ='shape');
    else:
        sel = cmds.ls(sn=True, typ='shape');
        seln = [];
        for i in sel:
            seln.append(getShapeName(i));
        sel = seln;
    for y in sel:
        if isRSLight(y) == 1:
            lightsRS.append(y);
    return lightsRS;

def getRSLights(type_name,formats):
    lightsTypeRS = [];
    lightsAll = getAllRSLights(formats);
    for i in lightsAll:
        if len(i.split(type_name))>1:
            lightsTypeRS.append(i);     
    return lightsTypeRS;

def makeLLink(obj,lights):
    cmds.lightlink(make = True, light=lights, object=obj );

def breakLLink(obj,lights):
    cmds.lightlink( b=True, light=lights, object=obj );

def makeSLink(obj,lights):
    cmds.lightlink(make = True, shadow = True, light=lights, object=obj );

def breakSLink(obj,lights):
    cmds.lightlink( b=True, shadow = True, light=lights, object=obj );

def exceptList(list, exclude_list):
    exclude_list_result = []
    for i in list:
        chk = 0;
        for k in exclude_list:
            if i == k:
                chk = 1;
        if chk == 0:
            exclude_list_result.append(i);
    return exclude_list_result;

def addCharsLink():
    sel = getSelection();
    lights_chars = getRSLights('chars_lights','long');
    lights_decor = getLongName(getRSLights('decor','short'));
    lights_decor_chars = exceptList(getLongName(getRSLights('chars','short')), lights_chars);
    makeLLink(sel,lights_chars);
    makeLLink(sel,lights_decor_chars);
    breakLLink(sel,lights_decor);
    makeSLink(sel,lights_chars);
    cmds.select(cl = True);

def removeCharsLink():
    sel = getSelection();
    lights_chars = getRSLights('chars_lights','long');
    lights_decor = getLongName(getRSLights('decor','short'));
    lights_decor_chars = exceptList(getLongName(getRSLights('chars','short')), lights_chars);
    breakLLink(sel,lights_chars);
    breakLLink(sel,lights_decor_chars);
    makeLLink(sel,lights_decor);
    breakSLink(sel,lights_chars);
    cmds.select(cl = True);

def addCharsShadowLink():
    sel = getSelection();
    lights_chars = getRSLights('chars_lights','long');
    makeSLink(sel,lights_chars);
    cmds.select(cl = True);

def deleteCharsShadowLink():
    sel = getSelection();
    lights_chars = getRSLights('chars_lights','long');
    breakSLink(sel,lights_chars);
    cmds.select(cl = True);

def resetLinkSet():
    lightsAll = getAllRSLights('long');
    sel = exceptList(cmds.ls(long=True, typ='shape'), lightsAll);
    makeLLink(sel,lightsAll);
    makeSLink(sel,lightsAll);
    cmds.select(cl = True);

def makeLinkSet_kids():
    resetLinkSet();
    sel = cmds.ls(sl = True);
    chars_sel = getSelection();
    chars_inv_sel = getInvertSelection(getSelection());
    lights_chars = getRSLights('chars_lights','long');
    lights_decor = getLongName(getRSLights('decor','short'));
    lights_decor_chars = exceptList(getLongName(getRSLights('chars','short')), lights_chars);
    breakLLink(chars_inv_sel,lights_chars);
    breakLLink(chars_inv_sel,lights_decor_chars);
    breakLLink(chars_sel,lights_decor);
    breakSLink(chars_inv_sel,lights_chars);
    cmds.select(cl = True);
