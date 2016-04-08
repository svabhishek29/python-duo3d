﻿  # -*- coding: utf-8 -*-

"""@package duo3d

    @brief:

    @author: Mateusz Owczarek (mateusz.owczarek@dokt.p.lodz.pl)
    @version: 0.1
    @date: April, 2016
    @copyright: 2016 (c) Mateusz Owczarek

    THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
    IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
    FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
    AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
    LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
    OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
    SOFTWARE.
"""

import os
import ctypes as ct

__all__ = ['CloseDUO', 'DUOFrame', 'DUOFrameCallback', 'DUOIMUSample', 'DUOInstance', 'DUOResolutionInfo',
		'DUO_ACCEL_2G', 'DUO_ACCEL_4G', 'DUO_ACCEL_16G', 'DUO_ACCEL_8G',
		'DUO_BIN_ANY', 'DUO_BIN_HORIZONTAL2', 'DUO_BIN_HORIZONTAL4', 'DUO_BIN_NONE', 'DUO_BIN_VERTICAL2', 'DUO_BIN_VERTICAL4',
		'DUO_GYRO_250', 'DUO_GYRO_500', 'DUO_GYRO_1000', 'DUO_GYRO_2000',
		'EnumerateResolutions', 'GetDUODeviceName', 'GetDUOFirmwareBuild', 'GetDUOFirmwareVersion', 'GetDUOSerialNumber',
		'GetLibVersion', 'OpenDUO', 'SetDUOResolutionInfo', 'StartDUO', 'StopDUO']  # TODO: Update this list

_duolib_path = os.path.join( os.path.dirname( __file__ ), "../DUOLib" )  # FIXME: Make it OS independent
_duolib = ct.cdll.LoadLibrary( _duolib_path )

# DUO instance
DUOInstance = ct.c_void_p

# DUO binning
DUO_BIN_ANY = -1
DUO_BIN_NONE = 0
DUO_BIN_HORIZONTAL2 = 1  # Horizontal binning by factor of 2
DUO_BIN_HORIZONTAL4 = 2  # Horizontal binning by factor of 4
DUO_BIN_VERTICAL2 = 4  # Vertical binning by factor of 2
DUO_BIN_VERTICAL4 = 8  # Vertical binning by factor of 4

class DUOResolutionInfo( ct.Structure ):
	"""
	DUO resolution info
	"""
	_fields_ = [
		( "width", ct.c_int ),
		( "height", ct.c_int ),
		( "binning", ct.c_int ),
		( "fps", ct.c_float ),
		( "minFps", ct.c_float ),
		( "maxFps", ct.c_float ),
	 ]

	def __init__( self ):
		super( ct.Structure, self ).__init__()

PDUOResolutionInfo = ct.POINTER( DUOResolutionInfo )

class DUOIMUSample( ct.Structure ):
	"""
	DUO IMU data sample
	"""
	_fields_ = [
		( "tempData", ct.c_float ),  # DUO temperature data
		( "accelData", ct.c_float * 3 ),  # DUO accelerometer data (x,y,z)
		( "gyroData", ct.c_float * 3 )  # DUO gyroscope data (x,y,z)
		 ]

	def __init__( self ):
		super( ct.Structure, self ).__init__()

DUO_MAX_IMU_SAMPLES = 100

class DUOFrame( ct.Structure ):
	"""
	DUOFrame structure holds the sensor data that is passed to user via DUOFrameCallback function
	"""
	_fields_ = [
		( "width", ct.c_uint32 ),  # DUO frame width
		( "height", ct.c_uint32 ),  # DUO frame height
		( "ledSeqTag", ct.c_uint8 ),  # DUO frame LED tag
		( "timeStamp", ct.c_uint32 ),  # DUO frame time stamp in 100us increments
		( "leftData", ct.POINTER( ct.c_uint8 ) ),  # DUO left frame data
		( "rightData", ct.POINTER( ct.c_uint8 ) ),  # DUO right frame data
		( "IMUPresent", ct.c_uint8 ),  # True if IMU chip is present ( DUO MLX )
		( "IMUSamples", ct.c_uint32 ),  # Number of IMU data samples in this frame
		( "IMUData", DUOIMUSample * DUO_MAX_IMU_SAMPLES )  # DUO IMU data samples
		 ]

	def __init__( self ):
		super( ct.Structure, self ).__init__()

PDUOFrame = ct.POINTER( DUOFrame )

class DUOLEDSeq( ct.Structure ):
	"""
	DUO LED PWM
	"""
	_fields_ = [
			( "ledPwmValue", ct.c_uint8 * 4 )  # LED PWM values are in percentage [0,100]
			]

	def __init__( self ):
		super( ct.Structure, self ).__init__()

PDUOLEDSeq = ct.POINTER( DUOLEDSeq )

# DUO Accelerometer Range
DUO_ACCEL_2G = 0  # DUO Accelerometer full scale range +/- 2g
DUO_ACCEL_4G = 1  # DUO Accelerometer full scale range +/- 4g
DUO_ACCEL_8G = 2  # DUO Accelerometer full scale range +/- 8g
DUO_ACCEL_16G = 3  # DUO Accelerometer full scale range +/- 16g

# DUO Gyroscope Range
DUO_GYRO_250 = 0  # DUO Gyroscope full scale range 250 deg/s
DUO_GYRO_500 = 1  # DUO Gyroscope full scale range 500 deg/s
DUO_GYRO_1000 = 2  # DUO Gyroscope full scale range 1000 deg/s
DUO_GYRO_2000 = 3  # DUO Gyroscope full scale range 2000 deg/s

class DUO_INTR( ct.Structure ):
	"""

	"""

	class INTR( ct.Structure ):
		_fields_ = [
				( "k1", ct.c_double ),  # Camera radial distortion coefficients
				( "k2", ct.c_double ),
				( "k3", ct.c_double ),
				( "k4", ct.c_double ),  # Camera radial distortion coefficients
				( "k5", ct.c_double ),
				( "k6", ct.c_double ),
				( "p1", ct.c_double ),  # Camera tangential distortion coefficients
				( "p2", ct.c_double ),
				( "fx", ct.c_double ),  # Camera focal lengths in pixel units
				( "fy", ct.c_double ),
				( "cx", ct.c_double ),  # Camera principal point
				( "cy", ct.c_double ),
				]

	_pack_ = 1
	_fields_ = [
			( "width", ct.c_uint32 ),
			( "height", ct.c_uint32 ),
			( "left", INTR ),
			( "right", INTR ),
			]

	def __init__( self ):
		super( ct.Structure, self ).__init__()

class DUO_EXTR( ct.Structure ):
	"""

	"""
	_pack_ = 1
	_fields_ = [
			( "rotation", ct.c_double * 9 ),
			( "translation", ct.c_double * 3 )
			]

	def __init__( self ):
		super( ct.Structure, self ).__init__()

class DUO_STEREO( ct.Structure ):
	"""

	"""
	_pack_ = 1
	_fields_ = [
			( "M1", ct.c_double * 9 ),  # 3x3 - Camera matrices
			( "M2", ct.c_double * 9 ),
			( "D1", ct.c_double * 8 ),  # 1x8 - Camera distortion parameters
			( "D2", ct.c_double * 8 ),
			( "R", ct.c_double * 9 ),  # 3x3 - Rotation between left and right camera
			( "T", ct.c_double * 3 ),  # 3x1 - Translation vector between left and right camera
			( "R1", ct.c_double * 9 ),  # 3x3 - Rectified rotation matrices
			( "R2", ct.c_double * 9 ),
			( "P1", ct.c_double * 12 ),  # 3x4 - Rectified projection matrices
			( "P2", ct.c_double * 12 ),
			( "Q", ct.c_double * 16 )  # 4x4 - Disparity to depth mapping matrix
			]

	def __init__( self ):
		super( ct.Structure, self ).__init__()

# DUO parameter unit
DUO_PERCENTAGE = 0
DUO_MILLISECONDS = 1

# DUO Camera parameters
DUO_DEVICE_NAME = 2  # Get only: ( string allocated by user min size 252 bytes )
DUO_SERIAL_NUMBER = 3  # Get only: ( string allocated by user min size 252 bytes )
DUO_FIRMWARE_VERSION = 4  # Get only: ( string allocated by user min size 252 bytes )
DUO_FIRMWARE_BUILD = 5  # Get only: ( string allocated by user min size 252 bytes )
DUO_RESOLUTION_INFO = 6  # Set/Get:  ( PDUOResolutionInfo ) - must be first parameter to set
DUO_FRAME_DIMENSION = 7  # Get only: ( uint32_t, uint32_t )
DUO_EXPOSURE = 8  # Set/Get:  ( double [ 0,100 ], DUO_PERCENTAGE ) or ( double in milliseconds, DUO_MILLISECONDS )
DUO_GAIN = 9  # Set/Get:  ( double [ 0,100 ] )
DUO_HFLIP = 10  # Set/Get:  ( bool [ false,true ] )
DUO_VFLIP = 11  # Set/Get:  ( bool [ false,true ] )
DUO_SWAP_CAMERAS = 12  # Set/Get:  ( bool [ false,true ] )

# DUO LED Control Parameters
DUO_LED_PWM = 13  # Set/Get:  ( double [ 0,100 ] )
DUO_LED_PWM_SEQ = 14  # Set only: ( PDUOLEDSeq, int ) - number of LED sequence steps ( max 64 )

# DUO Calibration Parameters
DUO_CALIBRATION_PRESENT = 15  # Get Only: return true if calibration data is present
DUO_FOV = 16  # Get Only: ( PDUOResolutionInfo, double* ( leftHFOV, leftVFOV, rightHFOV, rightVFOV )
DUO_UNDISTORT = 17  # Set/Get:  ( bool [ false,true ] )
DUO_INRINSICS = 18  # Get Only: ( pointer to DUO_INTR structure )
DUO_EXTRINSICS = 19  # Get Only: ( pointer to DUO_EXTR structure )
DUO_STEREO_PARAMETERS = 20  # Get Only: ( pointer to DUO_STEREO structure )

# DUO IMU Parameters
DUO_IMU_RANGE = 21  # Set/Get: ( DUOAccelRange, DUOGyroRange )

_duolib.GetLibVersion.argtypes = None
_duolib.GetLibVersion.restype = ct.c_char_p

def GetLibVersion():
	"""

	"""
	return _duolib.GetLibVersion()

# DUO resolution enumeration
_duolib.EnumerateResolutions.argtypes = [ ct.POINTER( DUOResolutionInfo ), ct.c_int32, ct.c_int32, ct.c_int32, ct.c_int32, ct.c_float ]
_duolib.EnumerateResolutions.restype = ct.c_int

def EnumerateResolutions( resList, resListSize, width = -1, height = -1, binning = DUO_BIN_ANY, fps = -1.0 ):
	"""
	Enumerates supported resolutions.
	To enumerate resolution settings for specific resolution, set width and height and optionally fps.
	To enumerate all supported resolutions set width, height and fps all to -1.
	@note: There are large number of resolution setting supported.
	@param resList:
	@param resListSize:
	@param width:
	@param height:
	@param binning:
	@param fps:
	@return: number of resolutions found
	"""
	return _duolib.EnumerateResolutions( ct.byref( resList ), resListSize, width, height, binning, fps )

# DUO device initialization
_duolib.OpenDUO.argtypes = [ ct.POINTER( DUOInstance ) ]
_duolib.OpenDUO.restype = ct.c_bool

def OpenDUO( duo ):
	"""
	Opens the DUO device and initialized the passed DUOInstance handle pointer.
	@param duo: DUOInstance handle pointer
	@return: True on success
	"""
	return _duolib.OpenDUO( ct.byref( duo ) )

_duolib.CloseDUO.argtypes = [ DUOInstance ]
_duolib.CloseDUO.restype = ct.c_bool

def CloseDUO( duo ):
	"""
	Closes the DUO device.
	@param duo: DUOInstance handle pointer
	@return: True on success
	"""
	return _duolib.CloseDUO( duo )

# DUO frame callback function
# NOTE: This function is called in the context of the DUO capture thread.
# 		 To prevent any dropped frames, this function must return as soon as possible.
DUOFrameCallback = ct.CFUNCTYPE( PDUOFrame, ct.c_void_p )

# DUO device capture control
_duolib.StartDUO.argtypes = [ DUOInstance, DUOFrameCallback, ct.c_void_p, ct.c_bool ]
_duolib.StartDUO.restype = ct.c_bool

def StartDUO( duo, frameCallback, pUserData, masterMode = True ):
	"""
	Starts capturing frames.
	@param duo: DUOInstance handle pointer
	@param frameCallback: pointer to user defined DUOFrameCallback callback function
	@param pUserData: any user data that needs to be passed to the callback function
	@param masterMode:
	@return: True on success
	"""
	callback = DUOFrameCallback( frameCallback )
	return _duolib.StartDUO( duo, callback, pUserData, masterMode )

_duolib.StopDUO.argtypes = [ DUOInstance ]
_duolib.StopDUO.restype = ct.c_bool

def StopDUO( duo ):
	"""
	Stops capturing frames.
	@param duo: DUOInstance handle pointer
	@return: True on success
	"""
	return _duolib.StopDUO( duo )

# DUO Camera parameters control
__DUOParamSet__ = _duolib[0x08]  # Cannot be imported by name due to underscores,
__DUOParamSet__.restype = ct.c_bool
__DUOParamGet__ = _duolib[0x07]  # ... therefore import by ordinals
__DUOParamGet__.restype = ct.c_bool

# Get DUO parameters
def GetDUODeviceName( duo ):
	"""

	"""
	val = ct.create_string_buffer( 260 )  # [5]
	__DUOParamGet__( duo, DUO_DEVICE_NAME, val )
	return val.value

def GetDUOSerialNumber( duo ):
	"""

	"""
	val = ct.create_string_buffer( 260 )  # [5]
	__DUOParamGet__( duo, DUO_SERIAL_NUMBER, val )
	return val.value

def GetDUOFirmwareVersion( duo ):
	"""

	"""
	val = ct.create_string_buffer( 260 )  # [5]
	__DUOParamGet__( duo, DUO_FIRMWARE_VERSION, val )
	return val.value

def GetDUOFirmwareBuild( duo ):
	"""

	"""
	val = ct.create_string_buffer( 260 )  # [5]
	__DUOParamGet__( duo, DUO_FIRMWARE_BUILD, val )
	return val.value

def GetDUOFrameDimension( duo, w, h ):
	"""

	"""
	# __DUOParamGet__(duo, DUO_FRAME_DIMENSION, (uint32_t*)w, (uint32_t*)h)
	raise NotImplementedError

def GetDUOExposure( duo, val ):
	"""

	"""
	# __DUOParamGet__(duo, DUO_EXPOSURE, (double*)val, DUO_PERCENTAGE)
	raise NotImplementedError

def GetDUOExposureMS( duo, val ):
	"""

	"""
	# __DUOParamGet__(duo, DUO_EXPOSURE, (double*)val, DUO_MILLISECONDS)
	raise NotImplementedError

def GetDUOGain( duo, val ):
	"""

	"""
	# __DUOParamGet__(duo, DUO_GAIN, (double*)val)
	raise NotImplementedError

def GetDUOHFlip( duo, val ):
	"""

	"""
	# __DUOParamGet__(duo, DUO_HFLIP, (int*)val)
	raise NotImplementedError

def GetDUOVFlip( duo, val ):
	"""

	"""
	#  __DUOParamGet__(duo, DUO_VFLIP, (int*)val)
	raise NotImplementedError

def GetDUOCameraSwap( duo, val ):
	"""

	"""
	# __DUOParamGet__(duo, DUO_SWAP_CAMERAS, (int*)val)
	raise NotImplementedError

def GetDUOLedPWM( duo, val ):
	"""

	"""
	# __DUOParamGet__(duo, DUO_LED_PWM, (double*)val)
	raise NotImplementedError

def GetDUOCalibrationPresent( duo ):
	"""

	"""
	# __DUOParamGet__(duo, DUO_CALIBRATION_PRESENT)
	raise NotImplementedError

def GetDUOFOV( duo, ri, val ):
	"""

	"""
	# __DUOParamGet__(duo, DUO_FOV, (DUOResolutionInfo&)ri, (double*)val)
	raise NotImplementedError

def GetDUOUndistort( duo, val ):
	"""

	"""
	# __DUOParamGet__(duo, DUO_UNDISTORT, (int*)val)
	raise NotImplementedError

def GetDUOIntrinsics( duo, val ):
	"""

	"""
	# __DUOParamGet__(duo, DUO_INRINSICS, (DUO_INTR*)val)
	raise NotImplementedError

def GetDUOExtrinsics( duo, val ):
	"""

	"""
	# __DUOParamGet__(duo, DUO_EXTRINSICS, (DUO_EXTR*)val)
	raise NotImplementedError

def GetDUOStereoParameters( duo, val ):
	"""

	"""
	# __DUOParamGet__(duo, DUO_STEREO_PARAMETERS, (DUO_STEREO*)val)
	raise NotImplementedError

def GetDUOIMURange( duo, accel, gyro ):
	"""

	"""
	# __DUOParamGet__(duo, DUO_IMU_RANGE, (int*)accel, (int*)gyro)
	raise NotImplementedError

# Set DUO parameters
def SetDUOResolutionInfo( duo, val ):
	"""
	Sets the desired resolution, binning and the frame rate
	@return: True on success
	"""
	# __DUOParamSet__(duo, DUO_RESOLUTION_INFO, (DUOResolutionInfo&)val)
	return __DUOParamSet__( duo, DUO_RESOLUTION_INFO, ct.byref( val ) )

def SetDUOExposure( duo, val ):
	"""

	@return: True on success
	"""
	#  __DUOParamSet__(duo, DUO_EXPOSURE, (double)val, DUO_PERCENTAGE)
	raise NotImplementedError

def SetDUOExposureMS( duo, val ):
	"""

	@return: True on success
	"""
	#  __DUOParamSet__(duo, DUO_EXPOSURE, (double)val, DUO_MILLISECONDS)
	raise NotImplementedError

def SetDUOGain( duo, val ):
	"""

	@return: True on success
	"""
	#  __DUOParamSet__(duo, DUO_GAIN, (double)val)
	raise NotImplementedError

def SetDUOHFlip( duo, val ):
	"""

	@return: True on success
	"""
	#  __DUOParamSet__(duo, DUO_HFLIP, (int)val)
	raise NotImplementedError

def SetDUOVFlip( duo, val ):
	"""

	@return: True on success
	"""
	#  __DUOParamSet__(duo, DUO_VFLIP, (int)val)
	raise NotImplementedError

def SetDUOCameraSwap( duo, val ):
	"""

	@return: True on success
	"""
	#  __DUOParamSet__(duo, DUO_SWAP_CAMERAS, (int)val)
	raise NotImplementedError

def SetDUOLedPWM( duo, val ):
	"""

	@return: True on success
	"""
	#  __DUOParamSet__(duo, DUO_LED_PWM, (double)val)
	raise NotImplementedError

def SetDUOLedPWMSeq( duo, val, size ):
	"""

	@return: True on success
	"""
	#  __DUOParamSet__(duo, DUO_LED_PWM_SEQ, (PDUOLEDSeq)val, (uint32_t)size)
	raise NotImplementedError

def SetDUOUndistort( duo, val ):
	"""

	@return: True on success
	"""
	#  __DUOParamSet__(duo, DUO_UNDISTORT, (int)val)
	raise NotImplementedError

def SetDUOIMURange( duo, accel, gyro ):
	"""
	Sets the IMU DUOAccelRange and DUOGyroRange range.
	@return: True on success
	"""
	return __DUOParamSet__( duo, DUO_IMU_RANGE, accel, gyro )
