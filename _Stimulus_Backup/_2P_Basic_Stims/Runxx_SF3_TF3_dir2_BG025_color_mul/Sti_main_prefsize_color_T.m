% Tang Rendong 20170317
clc; clear all;
global CRS;
vsgInit;
crsIOWriteDAC(0,'Volts5');  

deg2pix=32;
% deg2pix=20.7263;
% deg2pix=crsUnitToUnit(CRS.DEGREEUNIT, 1, CRS.PIXELUNIT);
framestep=2;

% Stimulus Parameters
Scan_mode=2;                 % 1 GA  2 RG
CenXY = round([-1.5,-1.5] *deg2pix);         
sizep=10;
Direction=[90:45:315];            % orientation 0 is H gratings move up, 90 is Vertical gratings moving left

sizem=sizep;
SF = [0.5 1 2];           % Spatial frequency  % Cycles per degree of visual angle
TF = [1 2 4] *framestep;

Nstim=length(SF)*length(TF)*length(Direction);  
Ntrials=7;                  

gratingtype =1;               % 1.square wave 0.sine wave
dutycycle = 0.4;              % white line is thiner if dutycycle > 0.5
time_ISI = 3;                 % Seconds.
time_on = 2;                  % Seconds.

curFrameRate= crsGetSystemAttribute(CRS.FRAMERATE);  % framerate of current system
cmSizep = round(sizep*deg2pix);
cmSizem = round(sizem*deg2pix);
totalframe=round(curFrameRate*time_on/framestep)+1;

bg=0.25; 
% mask
hs0=cmSizep/2;
x=1:cmSizem;  y=x;
rfx=repmat(x,length(x),1); rfx=rfx'; rfy=rfx';
mask0=sqrt((rfx-cmSizem/2).^2+(rfy-cmSizem/2).^2); 
mask0(mask0<=hs0)=1; mask0(mask0>hs0)=0; 
maskb=1-mask0;
maskb(maskb>0)=bg;

% Colour Definitions
blank=zeros(1024,1280,3)+bg;
crsSet24bitColourMode;
crsSetDrawPage(1); 
crsDrawMatrix24bitColour(blank); 
crsSetDrawPage(2); 
crsDrawMatrix24bitColour(blank); 

% 空间单位定义
viewdist=570;               
crsSetViewDistMM(viewdist);
crsSetSpatialUnits(CRS.PIXELUNIT);     % all units in degree of angles

% hostpages
hostpages=zeros(totalframe,1);
for n=1:totalframe
    hostpages(n) = crsPAGECreate(CRS.HOSTPAGE,[cmSizem,cmSizem], CRS.TRUECOLOURMODE)+1;    
    crsSetDrawPage(CRS.HOSTPAGE, hostpages(n),1);
end

% create condition file name
N_time=fix(clock);
logname=strcat('Sti main_gray_',num2str(N_time(4)),'_',num2str(N_time(5)),'_',num2str(N_time(6)),'.txt');

fprintf('press any key to start...\n');
pause;

% stimuli loop
for j=1:Ntrials  % trials
    stimindex=randperm(Nstim)';    % create and save condition file
%     stimindex=(1:Nstim)';        % create and save condition file

    fid=fopen(logname, 'a');
    fprintf(fid,'%2.0f\t',stimindex);  
    fclose(fid); 
    
    for i=1:Nstim      
        disp(['Ntrials= ', num2str(j)]);
        disp(['Current ID= ', num2str(stimindex(i))])
        [sfid, tfid, dirid]=ind2sub([length(SF),length(TF),length(Direction)],stimindex(i));          
        stimprep_Grat_sinewave_color_prefsize;

    % stimuli present
    if Scan_mode==1;  % GA才需对齐
    aa1=0; aa2=0;
    while 1;
        aa1=aa2; aa2=crsIOReadADC(0);     % disp([aa1,aa2]); pause(0.1);
        if aa2<aa1 && aa2>9000 && aa2<10000;
            break;
        end
    end
    end
    crsIOWriteDAC(5,'Volts5');

    start_step = clock; % Record reference time stamp at beginning of each loop.
    for n=1:totalframe-1
        crsSetDrawPage(2);
        crsSetDrawMode(CRS.CENTREXY);
        %copy pre-generated image from host page to vedio page.
        crsDrawMoveRect(CRS.HOSTPAGE, hostpages(n),[0,0],[cmSizem,cmSizem],CenXY,[cmSizem,cmSizem]);                
        %display current page.
        crsSetDisplayPage(2);
        crsSetDisplayPage(2); 
    end

    crsIOWriteDAC(0,'Volts5');  
    disp(etime(clock,start_step));
    crsSetDisplayPage(1); % Display background screen
    end
end
pause(time_ISI);  

