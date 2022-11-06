[filename, pathname] = uigetfile('*.*');
if isnumeric(filename); return; end   %user canceled
filename = fullfile(pathname, filename);
[fid, message] = fopen(filename, 'rt');
if fid < 0; error('Failed to open file "%s" because "%s"', filename, message); end
data = cell2mat( textscan(fid, '(%f)') );
fclose(fid)