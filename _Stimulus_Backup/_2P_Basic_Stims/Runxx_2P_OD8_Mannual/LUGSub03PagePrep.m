% HDGSub03PagePrep.m
% Prepare Stimulus (page 2, 3, 4, 5)
% only need specify: newstim (stim ID), testrun
% for page 2, fixation page, only color of the fixation dot changes from trial to trial
% for page 3, grating(a) page, currently draw grating with following variables:
%   gratingtype (1=square, 2=sine)
%   color
%   location
%   size
%   orientation (direction)
%   SF
%   velocity
%   fixation color
% for page 4, saccade page, only color of the saccade target dots changes from trial to trial
% for page 5, grating(b) page, currently draw grating with following variables (other parameters just copy from grating (a)):
%   SF, TF, orientation

%__________________________________________________ page 2: fixation dot 
crsSetDrawPage(CRS.VIDEOPAGE, 2, 1);            
crsSetPen1(fixcolor(newstim));
crsDrawOval([0,0], [fixsize, fixsize]); 
crsSetPen1(2);
crsDrawOval([0,0], [fixsize/3, fixsize/3]); 
if testrun
    crsSetDisplayPage(2);
    fprintf('Video page # 2: fixation dot... press any key to continue.\r');
    pause;
end


%__________________________________________________ page 3: grating page
crsSetDrawPage(CRS.VIDEOPAGE, 3, 1);            
% randomnize 999 values here 
% Sphase, Tphase, direction & orientation can be randomnized. 
if Sphase1(newstim)==999
    CSphase1=round(rand(1)*360);
else
    CSphase1=Sphase1(newstim);
end
if Tphase1(newstim)==999
    CTphase1=round(rand(1)*360);
else
    CTphase1=Tphase1(newstim);
end
if direction1(newstim)==999
    Cdirection1=double(round(rand(1))*2-1); % value 1 or -1
else
    Cdirection1=direction1(newstim);
end
if orientation1(newstim)==999
    Corientation1=round(rand(1)*360);
else
    Corientation1=orientation1(newstim);
end
if Sphase2(newstim)==999
    CSphase2=round(rand(1)*360);
else
    CSphase2=Sphase2(newstim);
end
if Tphase2(newstim)==999
    CTphase2=round(rand(1)*360);
else
    CTphase2=Tphase2(newstim);
end
if direction2(newstim)==999
    Cdirection2=double(round(rand(1))*2-1); % value 1 or -1
else
    Cdirection2=direction2(newstim);
end
if orientation2(newstim)==999
    Corientation2=round(rand(1)*360);
else
    Corientation2=orientation2(newstim);
end

% grating 1
objhandle1=crsObjCreate;
crsObjSetDefaults;
if gratingtype1(newstim)==1 | gratingtype1(newstim)==2
    if gratingtype1(newstim)==1
        tablesize=crsObjGetTableSize(CRS.SWTABLE);
        crsObjTableSquareWave(CRS.SWTABLE,round(tablesize*0),round(tablesize*dutycycle1(newstim)));     
    %   crsObjTableSquareWave(CRS.SWTABLE,round(tablesize*0.25),round(tablesize*0.75));        % half half
    elseif gratingtype1(newstim)==2
        crsObjTableSinWave(CRS.SWTABLE);
    end
    crsObjSetDriftVelocity(velocity1(newstim)*Cdirection1);
    crsObjSetSpatialPhase(CSphase1); 
end
if TF1(newstim)~=0
    crsObjSetTemporalFrequency(TF1(newstim));
    crsObjSetTemporalPhase(CTphase1); 
end
if TFtype1==1   % square wave
    crsObjTableSquareWave(CRS.TWTABLE,0,512);
elseif TFtype1==2 % sine wave
    crsObjTableSinWave(CRS.TWTABLE);
end
crsObjSetPixelLevels(pixtablelow1, npixlevel);
%crsObjSetColourVector(whitecolor1(newstim, :), blackcolor1(newstim,:), CRS.BIPOLAR);
crsObjSetColourVector(whitecolor1(newstim, :), blackcolor1(newstim,:), CRS.UNIPOLAR);
crsSetPen1(pixtablelow1);
crsSetPen2(pixtablelow1+npixlevel-1);
if gratingtype1(newstim)==1 | gratingtype1(newstim)==2
    pixLevsUsed = crsDrawGrating(wincenter1(newstim,:), winsize1(newstim,:), Corientation1, SF1(newstim));
elseif gratingtype1(newstim)==3
    Cesize1=10;
    Crddensity1=0.5;
    Cwincenter1pix=round(wincenter1(newstim,:)*deg2pix);
    map1=double(rand(round(winsize1(newstim).*deg2pix./Cesize1))<Crddensity1);
    if Cesize1~=1
        map1=imresize(map1, Cesize1);
    end
%    crsSetPen1(2);
    crsSetPen2((pixtablelow1+round(npixlevel-1)./2));    
    crsDrawMatrix(Cwincenter1pix, map1);
end


% grating 2
objhandle2=crsObjCreate;
crsObjSetDefaults;
if gratingtype2(newstim)==1
    tablesize=crsObjGetTableSize(CRS.SWTABLE);
    crsObjTableSquareWave(CRS.SWTABLE,round(tablesize*0),round(tablesize*dutycycle2(newstim)));     
elseif gratingtype2(newstim)==2
    crsObjTableSinWave(CRS.SWTABLE);
end
crsObjSetDriftVelocity(velocity2(newstim)*Cdirection2);
crsObjSetSpatialPhase(CSphase2); 
if TF1(newstim)~=0
    crsObjSetTemporalFrequency(TF2(newstim));
    crsObjSetTemporalPhase(CTphase2); 
end
if TFtype2==1   % square wave
    crsObjTableSquareWave(CRS.TWTABLE,0,512);
elseif TFtype2==2 % sine wave
    crsObjTableSinWave(CRS.TWTABLE);
end
crsObjSetPixelLevels(pixtablelow2, npixlevel);
crsObjSetColourVector(whitecolor2(newstim,:), blackcolor2(newstim,:), CRS.BIPOLAR);
crsSetPen1(pixtablelow2);
crsSetPen2(pixtablelow2+npixlevel-1);
pixLevsUsed = crsDrawGrating(wincenter2(newstim,:), winsize2(newstim,:), Corientation2,SF2(newstim));

crsSetPen1(fixcolor(newstim));
crsDrawOval([0,0], [fixsize, fixsize]); 
crsSetPen1(2);
crsDrawOval([0,0], [fixsize/3, fixsize/3]); 
if testrun
    crsPresent;
    fprintf('Video page # 3: cue stimulus... press any key to continue.\r');
    pause;
end


%__________________________________________________ page 5: 2nd grating page
% set following grating 1b parameters identical to grating 1
Cgratingtype1b=gratingtype1b(newstim);
Cdutycycle1b=dutycycle1(newstim);
Cvelocity1b=velocity1(newstim);
TFtype1b=TFtype1;
Cwhitecolor1b=whitecolor1(newstim, :);
Cblackcolor1b=blackcolor1(newstim, :);
Cwincenter1b=wincenter1(newstim, :);
Cwinsize1b=winsize1(newstim, :);

% set following grating 2b parameters identical to grating 2
Cgratingtype2b=gratingtype2b(newstim);
Cdutycycle2b=dutycycle2(newstim);
Cvelocity2b=velocity2(newstim);
TFtype2b=TFtype2;
Cwhitecolor2b=whitecolor2(newstim, :);
Cblackcolor2b=blackcolor2(newstim, :);
Cwincenter2b=wincenter2(newstim, :);
Cwinsize2b=winsize2(newstim, :);

% randomnize Sphase, Tphase here, 
if Sphase1b(newstim)==999
    CSphase1b=round(rand(1)*360);
elseif Sphase1b(newstim)==9999
    CSphase1b=CSphase1;
elseif Sphase1b(newstim)==99999
    CSphase1b=360-CSphase1;
end
if Tphase1b(newstim)==999
    CTphase1b=round(rand(1)*360);
elseif Tphase1b(newstim)==9999
    CTphase1b=CTphase1;
elseif Tphase1b(newstim)==99999
    CTphase1b=360-CTphase1;
end
if Sphase2b(newstim)==999
    CSphase2b=round(rand(1)*360);
elseif Sphase2b(newstim)==9999
    CSphase2b=CSphase2;
elseif Sphase2b(newstim)==99999
    CSphase2b=360-CSphase2;
end
if Tphase2b(newstim)==999
    CTphase2b=round(rand(1)*360);
elseif Tphase2b(newstim)==9999
    CTphase2b=CTphase2;
elseif Tphase2b(newstim)==99999
    CTphase2b=360-CTphase2;
end

% (note, direction, orientation didn't implemented randomnization yet, seems not so useful)
Corientation1b=orientation1b(newstim);
Corientation2b=orientation2b(newstim);
Cdirection1b=Cdirection1;
Cdirection2b=Cdirection2;

crsSetDrawPage(CRS.VIDEOPAGE, 5, 1);            
% grating 1b
objhandle1b=crsObjCreate;
crsObjSetDefaults;
if Cgratingtype1b==1
    tablesize=crsObjGetTableSize(CRS.SWTABLE);
    crsObjTableSquareWave(CRS.SWTABLE,round(tablesize*0),round(tablesize*Cdutycycle1b));     
elseif Cgratingtype1b==2
    crsObjTableSinWave(CRS.SWTABLE);
end
crsObjSetDriftVelocity(Cvelocity1b*Cdirection1b);
crsObjSetSpatialPhase(CSphase1b); 
if TF1b(newstim)~=0
    crsObjSetTemporalFrequency(TF1b(newstim));
    crsObjSetTemporalPhase(CTphase1b); 
end
if TFtype1b==1   % square wave
    crsObjTableSquareWave(CRS.TWTABLE,0,512);
elseif TFtype1b==2 % sine wave
    crsObjTableSinWave(CRS.TWTABLE);
end
crsObjSetPixelLevels(pixtablelow1b, npixlevel);
crsObjSetColourVector(Cwhitecolor1b, Cblackcolor1b, CRS.BIPOLAR);
%crsObjSetColourVector(Cwhitecolor1b, Cblackcolor1b, CRS.UNIPOLAR);
crsSetPen1(pixtablelow1b);
crsSetPen2(pixtablelow1b+npixlevel-1);
pixLevsUsed = crsDrawGrating(Cwincenter1b, Cwinsize1b, Corientation1b, SF1b(newstim));

% grating 2
objhandle2b=crsObjCreate;
crsObjSetDefaults;
if Cgratingtype2b==1
    tablesize=crsObjGetTableSize(CRS.SWTABLE);
    crsObjTableSquareWave(CRS.SWTABLE,round(tablesize*0),round(tablesize*Cdutycycle2b));     
elseif gratingtype2(newstim)==2
    crsObjTableSinWave(CRS.SWTABLE);
end
crsObjSetDriftVelocity(Cvelocity2b*Cdirection2b);
crsObjSetSpatialPhase(CSphase2b); 
if TF2b(newstim)~=0
    crsObjSetTemporalFrequency(TF2b(newstim));
    crsObjSetTemporalPhase(CTphase2b); 
end
if TFtype2b==1   % square wave
    crsObjTableSquareWave(CRS.TWTABLE,0,512);
elseif TFtype2b==2 % sine wave
    crsObjTableSinWave(CRS.TWTABLE);
end
crsObjSetPixelLevels(pixtablelow2b, npixlevel);
crsObjSetColourVector(Cwhitecolor2b, Cblackcolor2b, CRS.BIPOLAR);
crsSetPen1(pixtablelow2b);
crsSetPen2(pixtablelow2b+npixlevel-1);
pixLevsUsed = crsDrawGrating(Cwincenter2b, Cwinsize2b, Corientation2b, SF2b(newstim));

crsSetPen1(fixcolor(newstim));
crsDrawOval([0,0], [fixsize, fixsize]); 
crsSetPen1(2);
crsDrawOval([0,0], [fixsize/3, fixsize/3]); 
if testrun
    crsPresent;
    fprintf('Video page # 3: cue stimulus... press any key to continue.\r');
    pause;
end




%__________________________________________________ page 4: Saccade page
crsSetDrawPage(CRS.VIDEOPAGE, 4, 1);            
crsSetPen1(fixcolor(newstim));
crsDrawOval([-sccadex,0], [fixsize, fixsize]); 
crsDrawOval([sccadex,0], [fixsize, fixsize]); 
crsSetPen1(2);
crsDrawOval([-sccadex,0], [fixsize/3, fixsize/3]); 
crsDrawOval([sccadex,0], [fixsize/3, fixsize/3]); 
if testrun
    crsSetDisplayPage(4);
    fprintf('Video page # 4: saccade dots... press any key to continue.\r');   
    pause;
end
crsSetDisplayPage(1);




% output stim log
%fprintf('%d\t', fixcolor);

%  fixcolor
%  gratingtype1
%  wincenter1
%  size1
%  orientation1
%  direction1
%  velocity1
%  whitecolor1
%  blackcolor1
%  dutycycle1
%  SF1
%  Sphase1
%  TF1
%  Tphase1
%  gratingtype2
%  wincenter2
%  size2
%  orientation2
%  direction2
%  velocity2
%  whitecolor2
%  blackcolor2
%  dytycycle2
%  SF2
%  Sphase2
%  TF2
%  Tphase2

%fprintf(fid, '%f %f %f\t %d\t %f %f\t %f %f\t %d\t %d\t %f\t %f %f %f\t %f %f %f\t %f\t %f\t %f\t %f\t %f\t %f\t %d\t %f\t %d\r\n', ...
% fixcolor(newstim,:),	 gratingtype1(newstim),	 wincenter1(newstim,:),	 winsize1(newstim,:),	 Corientation1,	 Cdirection1,	 velocity1(newstim),	 whitecolor1(newstim,:),	 blackcolor1(newstim,:),	 dutycycle1(newstim),	 SF1(newstim),	 Sphase1(newstim),	 TF1(newstim),	 Tphase1(newstim));
