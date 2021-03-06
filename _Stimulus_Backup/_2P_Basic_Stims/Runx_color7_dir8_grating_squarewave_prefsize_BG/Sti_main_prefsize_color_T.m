% Tang Rendong 20170317
clc; clear all;
global CRS;
vsgInit;
crsIOWriteDAC(0,'Volts5');  
deg2pix=34.13;
% deg2pix=20.7263;
% deg2pix=crsUnitToUnit(CRS.DEGREEUNIT, 1, CRS.PIXELUNIT);
framestep=1;

% Stimulus Parameters
Scan_mode=1;  % 1 GA  2 RG
CenXY = [0,0] *deg2pix; % Degrees of visual angle 
sizep=5;
sizem=sizep;

Nstim=56;      %  
Ntrials=5;                  %repeat all stim 100 times; 
SF = 1;           % Spatial frequency  % Cycles per degree of visual angle
TF = 4 *framestep;

Orientation=-90:45:225;   % 0-180, use 999 for random, orientation 0 is H gratings move up, 90 is Vertical gratings moving left
Direction=0:45:315;   % 0-180, use 999 for random, orientation 0 is H gratings move up, 90 is Vertical gratings moving left
gratingtype =0;              %1.square wave 0.sine wave
dutycycle = 0.4;              % white line is thiner if dutycycle > 0.5
Velocity=TF/SF;
curFrameRate= crsGetSystemAttribute(CRS.FRAMERATE);  % framerate of current system
Vpixl=TF/SF *deg2pix/curFrameRate; % =2 

time_ISI = 3;                 % Seconds.
time_on = 2;                  % Seconds.
cmSizep = round(sizep*deg2pix);
cmSizem = round(sizem*deg2pix);
totalframe=round(curFrameRate*time_on/framestep)+1;
SizeP=sizep+Velocity/framestep*time_on*2+3;

% Colour Definitions
bg=0.1;                  % background 20
color(1,:)=[1,0,0]*0.6;   % 20     red
color(2,:)=[1,1,0]*0.27;  % 20    yellow
color(3,:)=[0,1,0]*0.32;  % 20    green
color(4,:)=[0,1,1]*0.3;   % 19.5    cyan
color(5,:)=[0,0,1]*1;     % 13.3   blue
color(6,:)=[1,0,1]*0.51; % 20    purple
color(7,:)=[1,1,1]*0.52;  % 20*2    white

% mask
hs0=cmSizep/2;
hs1=cmSizem/2;
x=1:cmSizem;  y=x;
rfx=repmat(x,length(x),1); rfx=rfx'; rfy=rfx';
mask0=sqrt((rfx-cmSizem/2).^2+(rfy-cmSizem/2).^2); 
mask0(mask0<=hs0)=1; mask0(mask0>hs0)=0;  % prefsize

maskb=zeros(cmSizem,cmSizem);
maskb=maskb+bg;

% Colour Definitions
blank=zeros(1024,1280,3)+bg;
crsSet24bitColourMode;
crsSetDrawPage(1); 
crsDrawMatrix24bitColour(blank); 
crsSetDrawPage(2); 
crsDrawMatrix24bitColour(blank); 

% 空间单位定义
viewdist=570;                 % in mm
crsSetViewDistMM(viewdist);
crsSetSpatialUnits(CRS.PIXELUNIT);     % all units in degree of angles

% hostpages
hostpages=zeros(totalframe,1);
for n=1:totalframe
    hostpages(n) = crsPAGECreate(CRS.HOSTPAGE,[cmSizem,cmSizem], CRS.TRUECOLOURMODE)+1;    
    crsSetDrawPage(CRS.HOSTPAGE, hostpages(n));
end

% create condition file name
N_time=fix(clock);
logname=strcat('Sti main_color_',num2str(N_time(4)),'_',num2str(N_time(5)),'_',num2str(N_time(6)),'.txt');

fprintf('press any key to start...\n');
pause;

% stimuli loop
for j=1:Ntrials  % trials
    stimindex=randperm(Nstim)';    % create and save condition file
%     stimindex=(1:Nstim)';    % create and save condition file
    
    fid=fopen(logname, 'a');
    fprintf(fid,'%2.0f\t',stimindex);  
    fclose(fid); 
    
    for i=1:Nstim     %   
        disp(['Ntrials= ', num2str(j)]);
        stimid=stimindex(i); 
        
        stimprep_grating_color;
           
        % stimuli present
        if Scan_mode==1;  % GA才需对齐
        aa1=0; aa2=0;
        while 1;
            aa1=aa2; aa2=crsIOReadADC(0);  %disp([aa1,aa2]);pause(0.1);
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
%             crsSetDisplayPage(2); 
        end

        crsIOWriteDAC(0,'Volts5');  
        disp(etime(clock,start_step));
        crsSetDisplayPage(1); % Display background screen
    end
end
pause(time_ISI);  

