#include <QCoreApplication>
#include <iostream>
#include <stdio.h>
#include <fstream>
#include <iomanip>
#include <sstream> //Just to record frames
#include <opencv2/opencv.hpp>
#include "stereocam.h"


double computeDistance(vector<int> box, Mat mask, Mat depth){
    vector<double> distances;
    for (int i=box[1];i<=box[3];++i){
        for(int j=box[0];j<=box[2];++j){
            if (mask.at<int>(i,j)==1)
                distances.push_back(depth.at<double>(i,j));
        }
    }
    return accumulate( distances.begin(), distances.end(), 0.0 )/ distances.size();;
}

int main(int argc, char *argv[])
{
    /*
    QCoreApplication a(argc, argv);

    //Record video
    stringstream ssLeft, ssRight;
    //string nameLeft = "/home/alex/Desktop/Alex stereo data/Extracted/Rectified/Left";
    //string nameRight = "/home/alex/Desktop/Alex stereo data/Extracted/Rectified/Right";
    //string nameDisparity = "/home/alex/Desktop/Alex stereo data/Extracted/Rectified/Disparity";
    //string type = ".png";
    // Read images sequence
    //string argL = "/home/francoisr/Documents/C++_Projects/Rectify Stereo/untitled/Images/Left/ImageL%05d.png";
    //VideoCapture sequenceL(argL);
    //string argR = "/home/francoisr/Documents/C++_Projects/Rectify Stereo/untitled/Images/Right/ImageR%05d.png";
    //VideoCapture sequenceR(argR);
    //string left_path = "/home/alex/Desktop/Alex stereo data/Extracted/left6.jpg";
    //string right_path = "/home/alex/Desktop/Alex stereo data/Extracted/right6.jpg";


    // input arguments
    string left_path = argv[1];
    string right_path = argv[2];
    string bboxPath = argv[3];
    string segMaskPath = argv[4];
    string nameDisparity = argv[5];
    string type = ".png";

    //Prepare the class stereocam and read the parameters
    StereoCam StereoRig;
    string filename ="/home/alex/Desktop/Alex stereo data/Extracted/StereoParamsAlex.yml";
    StereoRig.OpenParams(filename);

        // Load images
        //sequenceL >> ImageL;
        //sequenceR >> ImageR;
        Mat ImageL = imread(left_path,CV_LOAD_IMAGE_COLOR);
        Mat ImageR = imread(right_path,CV_LOAD_IMAGE_COLOR);
        ImageL.copyTo(StereoRig.ImageL);
        ImageR.copyTo(StereoRig.ImageR);

        // Rectify
        StereoRig.RectifyStereo();

        // Display
        //imshow("Rectified Left", StereoRig.ImageL_Rec);
        //imshow("Rectified Right", StereoRig.ImageR_Rec);
        //waitKey(1);

        //int aa = 6;
        // Save images
        /*
        vector<int> compression_params;
        compression_params.push_back(CV_IMWRITE_PNG_COMPRESSION);
        compression_params.push_back(9);

        ssLeft<<nameLeft<< setfill('0') << setw(5) << aa <<type;
        string filenameimwleft = ssLeft.str();
        ssLeft.str("");
        imwrite(filenameimwleft, StereoRig.ImageL_Rec, compression_params);

        ssRight<<nameRight<< setfill('0') << setw(5) << aa <<type;
        string filenameimwright = ssRight.str();
        ssRight.str("");
        imwrite(filenameimwright, StereoRig.ImageR_Rec, compression_params);
        */
        // Compute disparity
        /*
        Mat DispMap = StereoRig.ComputeDisparity(1,true);
        /*cv::rectangle(DispMap,cvPoint(457,281),
                      cvPoint(601,545),
                      CV_RGB(255,255,255), 5, 8);
        */
        //imshow("disp",DispMap);

        //save depth map
        /*
        vector<int> compression_params;
        compression_params.push_back(CV_IMWRITE_PNG_COMPRESSION);
        compression_params.push_back(9);
        ssLeft<<nameDisparity<< setfill('0') << setw(5) << aa <<type;
        string filenameimwdepth = ssLeft.str();
        imwrite(filenameimwdepth, DispMap, compression_params);

        // Depth from disparity
        StereoRig.ComputeDepthMap();
        /*double minDist = 100000;
        for (int i=457;i<=601;++i){
            for (int j=281;j<545;++j){
                minDist = min(minDist,StereoRig.DepthMap.at<double>(i,j));
            }
        }
        cout<< "Distance to the object = " << minDist << "m" << endl;
        */

        //write to file
        //cout<<"Startining writing to a file"<<endl;
        //FileStorage file("/home/alex/Desktop/Alex stereo data/Extracted/Rectified/depth6.yml", cv::FileStorage::WRITE);
        //file << "depth" << StereoRig.DepthMap;
        //cout<<"Writing to file is completed"<<endl;


        //new version for command line

        QCoreApplication a(argc, argv);

        // input arguments
        string left_path = argv[1];
        string right_path = argv[2];
        string bboxPath = argv[3];
        string segMaskPath = argv[4];
        string pathDisp = argv[5];
        string pathDist = argv[6];
        string type = ".png";

        //Prepare the class stereocam and read the parameters
        StereoCam StereoRig;
        StereoRig.OpenParams(segMaskPath);

            // Load images
            Mat ImageL = imread(left_path,CV_LOAD_IMAGE_COLOR);
            Mat ImageR = imread(right_path,CV_LOAD_IMAGE_COLOR);
            ImageL.copyTo(StereoRig.ImageL);
            ImageR.copyTo(StereoRig.ImageR);

            // Rectify
            StereoRig.RectifyStereo();

            // Display
            //imshow("Rectified Left", StereoRig.ImageL_Rec);
            //imshow("Rectified Right", StereoRig.ImageR_Rec);
            //waitKey(1);


            // Save images
            /*
            vector<int> compression_params;
            compression_params.push_back(CV_IMWRITE_PNG_COMPRESSION);
            compression_params.push_back(9);
            /*
            ssLeft<<nameLeft<< setfill('0') << setw(5) << aa <<type;
            string filenameimwleft = ssLeft.str();
            ssLeft.str("");
            imwrite(filenameimwleft, StereoRig.ImageL_Rec, compression_params);

            ssRight<<nameRight<< setfill('0') << setw(5) << aa <<type;
            string filenameimwright = ssRight.str();
            ssRight.str("");
            imwrite(filenameimwright, StereoRig.ImageR_Rec, compression_params);
            */

            // Compute disparity
            Mat DispMap = StereoRig.ComputeDisparity(1,true);
            //save depth map
            vector<int> compression_params;
            compression_params.push_back(CV_IMWRITE_PNG_COMPRESSION);
            compression_params.push_back(9);
            imwrite(pathDisp, DispMap, compression_params);

            // Depth from disparity
            StereoRig.ComputeDepthMap();

            //read bounding boxes
            vector<vector<int> > bboxVector;
            ifstream myfile (bboxPath);
              if (myfile.is_open())
              {
                string line;
                while ( getline (myfile,line) )
                {
                  istringstream iss(line);
                  vector<int> temp;
                  for(string s; iss >> s; ){
                      temp.push_back(stoi(s));
                  }

                  bboxVector.push_back(temp);
                }
                myfile.close();
              }
              else cout << "Unable to open file";

            //read segmentation mask
            Mat segMask = imread(segMaskPath,CV_LOAD_IMAGE_COLOR);
            //imshow("disp",segMask);

            //calculate distance to the object
            vector<double> distVector;
            for (int i =0; i<bboxVector.size();++i){
                double dist = computeDistance(bboxVector[i],segMask, StereoRig.DepthMap);
                distVector.push_back(dist);
            }

            ofstream myfile1;
            myfile1.open (pathDist);
            for (int i =0; i<distVector.size();++i)
                myfile1 << distVector[i] << endl;
            myfile1.close();

    return a.exec();
}

