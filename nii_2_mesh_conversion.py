import vtk
import argparse
parser = argparse.ArgumentParser(description='Convert .nii files to .stl')
parser.add_argument('infile', type=str, help='Input file (.nii)')
parser.add_argument('outfile', type=str, help='Output file (no suffix)')
args = parser.parse_args()
print('the infile is')
print(args.infile)
print('the outfile is')
print(args.outfile)
def nii_2_mesh (infile, outfile, label):

    """
    Read a nifti file including a binary map of a segmented organ with label id = label. 
    Convert it to a smoothed mesh of type stl.

    args.infile     : Input nifti binary map 
    filename_stl     : Output mesh name in stl format
    label            : segmented label id 
    """

    # read the file
    reader = vtk.vtkNIFTIImageReader()
    reader.SetFileName(args.infile)
    reader.Update()
    
    # apply marching cube surface generation
    surf = vtk.vtkDiscreteMarchingCubes()
    surf.SetInputConnection(reader.GetOutputPort())
    surf.SetValue(0, label) # use surf.GenerateValues function if more than one contour is available in the file
    surf.Update()
    
    #smoothing the mesh
    smoother= vtk.vtkWindowedSincPolyDataFilter()
    if vtk.VTK_MAJOR_VERSION <= 5:
        smoother.SetInput(surf.GetOutput())
    else:
        smoother.SetInputConnection(surf.GetOutputPort())
    smoother.SetNumberOfIterations(30) 
    smoother.NonManifoldSmoothingOn()
    smoother.NormalizeCoordinatesOn() #The positions can be translated and scaled such that they fit within a range of [-1, 1] prior to the smoothing computation
    smoother.GenerateErrorScalarsOn()
    smoother.Update()
     
    # save the output
    writer = vtk.vtkSTLWriter()
    writer.SetInputConnection(smoother.GetOutputPort())
    writer.SetFileTypeToASCII()
    writer.SetFileName(args.outfile)
    writer.Write()
if __name__ == '__main__':
    
    #args.infile =  'test.nii.gz'
    #args.outfile = 'test.stl'
    label = 1
    nii_2_mesh (args.infile, args.outfile, label)
