# Inclusion MRIs
IMA_T1MRI_INC = 't1mri_inclusion.nii.gz'
IMA_T2MRI_INC = 't2mri_inclusion.nii.gz'

# Pre-op MRIs (with frame)
IMA_T1MRI_PRE = 't1mri_pre.nii.gz'
IMA_T2MRI_PRE = 't2mri_pre.nii.gz'
# ADDS for Pitie T2 CORO Interlace Case
IMA_T2MRI_1MM_PRE = 't2mri_1mm_pre.nii.gz'
IMA_T2MRI_INTERLACED_PRE = 't2mri_interlaced_pre.nii.gz'

# MRIs of reference for segmentation: inclusion if they exist, otherwise pre-op
IMA_T1MRI = 't1mri.nii.gz'
IMA_T2MRI = 't2mri.nii.gz'
# ADDS for Pitie T2 CORO Interlace Case
IMA_T2MRI_1MM = 't2mri_1mm.nii.gz'
IMA_T2MRI_INTERLACED = 't2mri_interlaced.nii.gz'
IMA_T1MRI_POST = 't1mri_post.nii.gz'
# CT pre- and post-op
IMA_CTPRE = 'ct_pre.nii.gz'
IMA_CTPOST = 'ct_post.nii.gz'

IMA_CTPOST_VOLTAGE_LEFT = 'ct_post_voltage_left.nii.gz'
IMA_CTPOST_VOLTAGE_RIGHT = 'ct_post_voltage_right.nii.gz'

# Anatomo-clinical atlas
CLINICAL_ATLAS = 'clinical_atlas.nii.gz'

# Cropped images
CROP_LEFT_ELECTRODE = 'crop_left_electrode.nii.gz'
CROP_RIGHT_ELECTRODE = 'crop_right_electrode.nii.gz'

# Registered images
REGIMA_T2MRI2T1MRI = 't2mri_2_t1mri.nii.gz'
REGIMA_T1MRIPOST2T1MRI = 't1mri_post_2_t1mri.nii.gz'

REGIMA_CTPRE2T1MRI = 'ct_pre_2_t1mri.nii.gz'
REGIMA_CTPOST2CTPRE = 'ct_post_2_ct_pre.nii.gz'
REGIMA_INTERLACEDT2MRI2T1MRI = 't2mri_interlaced_2_t1mri.nii.gz'
REGIMA_CTPOST2T1MRI = 'ct_post_2_t1mri.nii.gz'

# XFM registration matrices (fsl and world-2-world)

REGMAT_T1MRI2CTPRE = 't1mri_2_ctpre.xfm'
REGMAT_T1MRI2CTPOST = 't1mri_2_ctpost.xfm'
REGMAT_T1MRI2ACPC = 't1mri_2_acpc.xfm'
REGMAT_T1MRI2PARK = 't1mri_2_park.xfm'
REGMAT_T2MRI2PARK = 't2mri_2_park.xfm'
REGMAT_T1MRI2YEB_LH = 'lh_t1mri_2_yeb.xfm'
REGMAT_T1MRI2YEB_RH = 'rh_t1mri_2_yeb.xfm'

REGMAT_T1MRIPOST2T1MRI = 't1mri_post_2_t1mri.xfm'
REGMAT_T1MRI2T1MRI_POST= 't1mri_2_t1mri_post.xfm'

REGMAT_T2MRI2T1MRI = 't2mri_2_t1mri.xfm'
REGMAT_T2MRI2ACPC = 't2mri_2_acpc.xfm'
REGMAT_INTERLACEDT2MRI2T1MRI = 't2mri_interlaced_2_t1mri.xfm'
REGMAT_INTERLACEDT2MRI2ACPC = 't2mri_interlaced_2_acpc.xfm'

REGMAT_CTPRE2T1MRI = 'ct_pre_2_t1mri.xfm'
REGMAT_CTPRE2ACPC = 'ctpre_2_acpc.xfm'

REGMAT_CTPOST2CTPRE = 'ct_post_2_ctpre.xfm'

REGMAT_CTPOST2T1MRI = 'ct_post_2_t1mri.xfm'
REGMAT_CTPOST2ACPC = 'ctpost_2_acpc.xfm'
REGMAT_CTPOST2PARK = 'ctpost_2_park.xfm'
REGMAT_CTPOST2CROPLEFT = 'ctpost_2_crop_left.xfm'
REGMAT_CTPOST2CROPRIGHT = 'ctpost_2_crop_right.xfm'

REGMAT_FRAME2CTPRE_INIT = 'frame_2_ctpre_init.xfm'
REGMAT_FRAME2CTPRE = 'frame_2_ctpre.xfm'
REGMAT_FRAME2ACPC = 'frame_2_acpc.xfm'
REGMAT_FRAME2T1MRIPRE = 'frame_2_t1mripre_init.xfm'

REGMAT_PARK2T1MRI = 'park_2_t1mri.xfm'
REGMAT_PARK2ACPC =  'park_2_acpc.xfm'
REGMAT_YEB2T1MRI_LH = 'yeb_2_lh_t1mri.xfm'
REGMAT_YEB2T1MRI_RH = 'yeb_2_rh_t1mri.xfm'

REG_MAT_AXIAL_ELECTRODE_LEFT= 'axial_electrode_left.xfm'
REG_MAT_AXIAL_ELECTRODE_RIGHT= 'axial_electrode_right.xfm'
REG_MAT_SAGITTAL_ELECTRODE_LEFT= 'sagittal_electrode_left.xfm'
REG_MAT_SAGITTAL_ELECTRODE_RIGHT= 'sagittal_electrode_right.xfm'
REG_MAT_CORONAL_ELECTRODE_LEFT= 'coronal_electrode_left.xfm'
REG_MAT_CORONAL_ELECTRODE_RIGHT= 'coronal_electrode_right.xfm'

MAT_FSL = 'fsl'
MAT_WORLD2WORLD = 'w2w'
MAT_SLICER = 'slicer'


# Prefixes for referentials
REF_T1MRI = 'ref_t1mri'
REF_T1MRIPRE = 'ref_t1mripre'
REF_CTPRE = 'ref_ctpre'
REF_CTPOST = 'ref_ctpost'
REF_PARK = 'ref_park'

# Mmasks
MASK_HEAD = 'head.nii.gz'
MASK_BRAIN = 'brain.nii.gz'
MASK_WM = 'brain_wm.nii.gz'
MASK_GM = 'brain_gm.nii.gz'
MASK_CSF = 'brain_csf.nii.gz'
MASK_CORTEX_LEFT = 'cortex_left.nii.gz'
MASK_CORTEX_RIGHT = 'cortex_right.nii.gz'
MASK_SKULL = 'skull.nii.gz'
MASK_SKIN = 'skin.nii.gz'
MASK_SKIN_EDGES = 'skin_edges.nii.gz'
MASK_PARKINSON_ATLAS = 'park_atlas.nii.gz'
MASK_PARKINSON_ATLAS_LINEAR = 'park_atlas_linear.nii.gz'
MASK_ELECTRODE_LEFT = 'electrode_left.nii.gz'
MASK_ELECTRODE_RIGHT = 'electrode_right.nii.gz'
MASK_FRAME_ARTIFACT_LEFT = 'frame_artifact_left.nii.gz'
MASK_FRAME_ARTIFACT_RIGHT = 'frame_artifact_right.nii.gz'
MASK_FRAME_ARTIFACT_ANTERIOR = 'frame_artifact_anterior.nii.gz'
MASK_FRAME_ARTIFACT = 'frame_artifact.nii.gz'
MASK_FRAME_ARTIFACT_CC = 'frame_artifact_cc.nii.gz'
MASK_FRAME_MODEL = 'frame_model.nii.gz'
MASK_SUPPORTS = 'frame_supports.nii.gz'

# Stimulation voltage
MASK_VOLTAGE_LEFT = 'voltage_left.nii.gz'
MASK_VOLTAGE_RIGHT = 'voltage_right.nii.gz'
MASK_VOLTAGE = 'voltage.nii.gz'


# Masked images
MASKED_T1MRI_BRAIN = 't1mri_brain.nii.gz'
MASKED_T1MRI_HEAD = 't1mri_head.nii.gz'
MASKED_T1MRI_HEAD_UNBIASED = 't1mri_head_unbiased.nii.gz'
MASKED_CTPOST_CORTEX_LEFT = 'ctpost_cortex_left.nii.gz'
MASKED_CTPOST_CORTEX_RIGHT = 'ctpost_cortex_right.nii.gz'

# Meshes
MESH_SULCI = 'sulci.vtk'
MESH_SULCI_LEFT = 'sulci_left.vtk'
MESH_SULCI_RIGHT = 'sulci_right.vtk'
MESH_HEAD = 'head.vtk'
MESH_SKIN_EDGES = 'skin_edges.vtk'
MESH_GRAY_PIAL_LEFT = 'cortex_gray_pial_left.vtk'
MESH_GRAY_PIAL_RIGHT = 'cortex_gray_pial_right.vtk'
MESH_GRAY_WHITE_LEFT = 'cortex_gray_white_left.vtk'
MESH_GRAY_WHITE_RIGHT = 'cortex_gray_white_right.vtk'
MESH_SKULL = 'skull.vtk'
MESH_SKIN = 'skin.vtk'
MESH_AC = 'landmark_ac.vtk'
MESH_PC = 'landmark_pc.vtk'
MESH_IH = 'landmark_ih.vtk'
MESH_PARKINSON_ATLAS = 'park_atlas.vtk'
MESH_ELECTRODE_LEFT = 'electrode_left.vtk'
MESH_ELECTRODE_RIGHT = 'electrode_right.vtk'
MESH_ELECTRODE_MODEL_AXIS_LEFT = 'electrode_model_axis_left.vtk'
MESH_ELECTRODE_MODEL_AXIS_RIGHT = 'electrode_model_axis_right.vtk'
MESH_ELECTRODE_MODEL_CONTACTS_LEFT = 'electrode_model_contacts_left.vtk'
MESH_ELECTRODE_MODEL_CONTACTS_RIGHT = 'electrode_model_contacts_right.vtk'
MESH_FRAME_ARTIFACT = 'frame_artifact.vtk'
MESH_FRAME_POINTS = 'frame_points.vtk'
MESH_FRAME_MODEL = 'frame_model.vtk'
MESH_SUPPORTS = 'frame_supports.vtk'
BAR_MESH_ELECTRODE_LEFT = 'electrode_curve_left.vtk'
BAR_MESH_ELECTRODE_RIGHT = 'electrode_curve_right.vtk'

MESH_INSERTION_ZONE_LEFT='insertion_zone_left.vtk'
MESH_INSERTION_ZONE_RIGHT='insertion_zone_right.vtk'


MESH_PREOP_TRAJECTORY_SELECTED_LEFT = 'preop_trajectory_selected_left.vtk'
MESH_PREOP_TRAJECTORY_SELECTED_RIGHT = 'preop_trajectory_selected_right.vtk'
MESH_PREOP_TRAJECTORY_NONSELECTED_LEFT = 'preop_trajectory_nonselected_left.vtk'
MESH_PREOP_TRAJECTORY_NONSELECTED_RIGHT = 'preop_trajectory_nonselected_right.vtk'

# Parkinson template meshes
MESH_PARK_AMYGDALA_LEFT='amygdala_left.vtk'
MESH_PARK_AMYGDALA_RIGHT='amygdala_right.vtk'
MESH_PARK_CAUDATE_LEFT='caudate_left.vtk'
MESH_PARK_CAUDATE_RIGHT='caudate_right.vtk'
MESH_PARK_GPE_LEFT='gpe_left.vtk'
MESH_PARK_GPE_RIGHT='gpe_right.vtk'
MESH_PARK_GPI_LEFT='gpi_left.vtk'
MESH_PARK_GPI_RIGHT='gpi_right.vtk'
MESH_PARK_HIPPOCAMPUS_LEFT='hippocampus_left.vtk'
MESH_PARK_HIPPOCAMPUS_RIGHT='hippocampus_right.vtk'
MESH_PARK_LGN_LEFT='lateral_geniculate_left.vtk'
MESH_PARK_LGN_RIGHT='lateral_geniculate_right.vtk'
MESH_PARK_MGN_LEFT='medial_geniculate_left.vtk'
MESH_PARK_MGN_RIGHT='medial_geniculate_right.vtk'
MESH_PARK_PUTAMEN_LEFT='putamen_left.vtk'
MESH_PARK_PUTAMEN_RIGHT='putamen_right.vtk'
MESH_PARK_REDNUCLEUS_LEFT='red_nucleus_left.vtk'
MESH_PARK_REDNUCLEUS_RIGHT='red_nucleus_right.vtk'
MESH_PARK_STN_LEFT='stn_left.vtk'
MESH_PARK_STN_RIGHT='stn_right.vtk'
MESH_PARK_SUBSTNIGRA_LEFT='substantia_nigra_left.vtk'
MESH_PARK_SUBSTNIGRA_RIGHT='substantia_nigra_right.vtk'
MESH_PARK_THALAMUS_LEFT='thalamus_left.vtk'
MESH_PARK_THALAMUS_RIGHT='thalamus_right.vtk'
MESH_PARK_LATVENTRICLE_LEFT='lateral_ventricle_left.vtk'
MESH_PARK_LATVENTRICLE_RIGHT='lateral_ventricle_right.vtk'
MESH_PARK_THIRDVENTRICLE='third_ventricle.vtk'
MESH_PARK_FOURTHVENTRICLE='fourth_ventricle.vtk'
MESH_PARK_TENT_LEFT='tent_left.vtk'
MESH_PARK_TENT_RIGHT='tent_right.vtk'
MESH_PARK_FALX='falx.vtk'


# Color LUT
PARK_COLOR_TABLE = 'park_color_table.ctbl'
YEB_COLOR_TABLE = 'yeb_color_table.ctbl'
VOLTAGE_COLOR_TABLE = 'voltage_color_table.ctbl'

# MRML scenes
MRML_SCENE_INCLUSION = 'scene_inclusion.mrml'
MRML_SCENE_PREOP = 'scene_preop.mrml'
MRML_SCENE_PREOP_PITIE = 'scene_preop_pitie.mrml'

MRML_SCENE_PREOP_ELECTRODE_LEFT = 'scene_preop_electrode_left.mrml'
MRML_SCENE_PREOP_ELECTRODE_RIGHT = 'scene_preop_electrode_right.mrml'

MRML_SCENE_POSTOP = 'scene_postop.mrml'
MRML_SCENE_MNI = 'scene_MNI.mrml'
MRML_SCENE_POSTOP_VOLTAGE = 'scene_postop_voltage.mrml'
MRML_SCENE_POSTOP_ELECTRODE_LEFT = 'scene_postop_electrode_left.mrml'
MRML_SCENE_POSTOP_ELECTRODE_RIGHT = 'scene_postop_electrode_right.mrml'
MRML_SCENE_YEB = 'scene_yeb.mrml'

# Trajectories
INCLUSION_TRAJECTORY_MANUAL = 'inclusion_trajectory_manual.xml'
INCLUSION_TRAJECTORY_AUTOMATIC = 'inclusion_trajectory_automatic.xml'
LEKSELL_TRAJECTORY = 'leksell_trajectory.xml'


# =============== OTHER CONSTANTS ==============


SCENE_TYPE_INCLUSION = "INCLUSION"
SCENE_TYPE_PREOP = "PREOP"
SCENE_TYPE_PREOP_PROBE_EYE_LEFT = "PREOP_PROB_EYE_LEFT"
SCENE_TYPE_PREOP_PROBE_EYE_RIGHT = "PREOP_PROB_EYE_RIGHT"
SCENE_TYPE_POSTOP = "POSTOP"
SCENE_TYPE_POSTOP_PROBE_EYE_LEFT = "POSTOP_PROB_EYE_LEFT"
SCENE_TYPE_POSTOP_PROBE_EYE_RIGHT = "POSTOP_PROB_EYE_RIGHT"

INCLUSION_TRAJECTORY_TYPE_MANUAL="MANUAL"
INCLUSION_TRAJECTORY_TYPE_AUTOMATIC="AUTOMATIC"
INCLUSION_TRAJECTORY_SPACE_ACPC = "ACPC"
INCLUSION_TRAJECTORY_SPACE_T1MRI = "T1MRI"
INCLUSION_TRAJECTORY_CONVENTION_RAS = "RAS"
INCLUSION_TRAJECTORY_CONVENTION_LPS = "LPS"


# Electrodes parameters
ELECTRODE_3387 = '3387'
ELECTRODE_3389 = '3389'

ELECTRODE_3387_CONTACT_DISTAL_TIP_OFFSET = 1.5
ELECTRODE_3387_CONTACT_LENGTH = 1.5
ELECTRODE_3387_CONTACT_SPACING = 1.5
ELECTRODE_3387_CONTACT_NUMBER = 4
ELECTRODE_3387_DIAMETER = 1.27

ELECTRODE_3389_CONTACT_DISTAL_TIP_OFFSET = 1.5
ELECTRODE_3389_CONTACT_LENGTH = 1.5
ELECTRODE_3389_CONTACT_SPACING = 0.5
ELECTRODE_3389_CONTACT_NUMBER = 4
ELECTRODE_3389_DIAMETER = 1.27

EPILEPSY_ELECTRODE_CONTACT_DISTAL_TIP_OFFSET = 1
EPILEPSY_ELECTRODE_CONTACT_LENGTH = 2.3
EPILEPSY_ELECTRODE_CONTACT_SPACING = 2.7
EPILEPSY_ELECTRODE_DIAMETER = 1

EPILEPSY_ELECTRODE_MICRO_CONTACT_DISTAL_TIP_OFFSET = 0.2 # We have to ask
EPILEPSY_ELECTRODE_MICRO_CONTACT_LENGTH = 1.57
EPILEPSY_ELECTRODE_MICRO_CONTACT_SPACING = 5.43
EPILEPSY_ELECTRODE_MICRO_CONTACT_1_2_SPACING = 1.43
EPILEPSY_ELECTRODE_MICRO_DIAMETER = 1

EPILEPSY_ELECTRODE_SCREW_THIN_LENGTH = 18.4
EPILEPSY_ELECTRODE_SCREW_THIN_DIAMETER = 2.5
EPILEPSY_ELECTRODE_SCREW_THICK_LENGTH = 8.8
EPILEPSY_ELECTRODE_SCREW_THICK_DIAMETER = 4.5 #7.1

# Leksell trajectory offset (mm)
LEKSELL_TRAJECTORY_OFFSET = 2
TRAJECTORY_TUBE_DIAMETER = 1.27

# Thresholds for electrode segmentation
THRESHOLD_ELECTRODE_LOW = 2500
THRESHOLD_ELECTRODE_HIGH = 4000

# Parameters for electrode detection (in mm)
OFFSET_BETWEEN_ELECTRODE_ARTIFACT_AND_ELECTRODE_TIP = 0.83
ARTIFACT_LENGTH_FOR_DIRECTION_ESTIMATION = 15

# Slice reformat transform types
SLICE_TYPE_AXIAL = 'Axial'
SLICE_TYPE_CORONAL = 'Coronal'
SLICE_TYPE_SAGITTAL = 'Sagittal'

SLICE_COLOR_AXIAL = 'Red'
SLICE_COLOR_SAGITTAL = 'Yellow'
SLICE_COLOR_CORONAL = 'Green'


# Lateralities
LATERALITY_LEFT = 'LEFT'
LATERALITY_RIGHT = 'RIGHT'
LATERALITY_BOTH = 'BOTH'

# Targets
TARGET_NST = "NST"
TARGET_GPI = "GPI"
TARGET_VIM = "VIM"

# Trajectory types
TRAJECTORY_CENTRAL = 'C'
TRAJECTORY_INTERNAL = 'I'
TRAJECTORY_EXTERNAL = 'E'
TRAJECTORY_ANTERIOR = 'A'
TRAJECTORY_POSTERIOR = 'P'

SELECTED = 'SELECTED'
NON_SELECTED = 'NON_SELECTED'

# Pipelines
PIPELINE_INCLUSION = 0
PIPELINE_INCLUSION_PITIE = 5
PIPELINE_PREOP= 1
PIPELINE_POSTOP= 2
PIPELINE_POSTOP_PITIE = 6
PIPELINE_PREOP_PITIE = 3
PIPELINE_ALL= 4

# criteria for dicomserie inclusion
CT_MIN_SLICES = 100
T1_MIN_SLICES = 100
T2_MIN_SLICES = 0
DTI_MIN_SLICES = 10


IMAGE_TYPE_CT = 'CT'
IMAGE_TYPE_T1MRI = 'T1_MRI'
IMAGE_TYPE_T2MRI = 'T2_MRI'
IMAGE_TYPE_DTI = 'DTI'

# stimulation
SIGMA_GRAY_MATTER = 0.33e-3

POSITIVE = "Positive"
NEGATIVE = "Negative"

LEFT = "LEFT"
RIGHT = "RIGHT"
BOTH = "BOTH"

ENTRY = "ENTRY"
TARGET = "TARGET"

# Trajectory names
TRAJECTORY_CENTRAL_NAME = 'Central'
TRAJECTORY_INTERNAL_NAME = 'Interior'
TRAJECTORY_EXTERNAL_NAME = 'Exterior'
TRAJECTORY_ANTERIOR_NAME = 'Anterior'
TRAJECTORY_POSTERIOR_NAME = 'Posterior'

# Parkinson template ROI
PARK_T1ROI_ORIGIN =  [53,80,45]
PARK_T1ROI_SIZE = [85,85,65]

PARK_T2ROI_ORIGIN =  [53,80+24,45+22]
PARK_T2ROI_SIZE = [85,36,38]

# Clinical scores
UPDRS1 = 'UPDRS1'
UPDRS2 = 'UPDRS2'
UPDRS3 = 'UPDRS3'
MADRS = 'MADRS'
MDRS = 'MDRS'
EKMAN = 'EKMAN'
UPDRS1 = 'UPDRS1'
AMDPAT = 'AMDPAT'
AES = 'AES'
UPDRS4 = 'UPDRS4'
HOEHN = 'HOEHN&YAHR'
SCHWAB = 'SCHWAB&ENGLAND'
TMT_A = 'TMT_A'
TMT_B = 'TMT_B'
TMT_B_A = 'TMT_B-A'
FLUENCES_LEX = 'FLUENCES_LEX'
FLUENCES_CAT = 'FLUENCES_CAT'
FLUENCES_VER = 'FLUENCES_VER'
STROOP = 'STROOP'

# Phases of the scores
Y_1 = '-1Y'
M_3 = '-3M'
M3 = '3M'
M6 = '6M'
Y1 = '1Y'
Y2 = '2Y'
Y3 = '3Y'
Y4 = '4Y'
Y5 = '5Y'
Y6 = '6Y'
Y7 = '7Y'
Y10 = '10Y'

# Names of the anatomo-clinical atlases
PROB_MONO = 'Prob mono'
STAT_MONO = 'Stat mono'
PROB_MULTI = 'Prob multi'
STAT_MULTI = 'Stat multi'

# Disease names
PARKINSON = 'PARKINSON'
DYSTONIA = 'DYSTONIE'
GDLT = 'GILLES DE LA TOURETTE'
TREM = 'TREMBLEMENT ESSENTIEL'
TOC = 'TOC'

# Target names
GPI = 'GPI'
NST = 'NST'
VIM = 'VIM'


# referentials
LEKSELL = 'Leksell'

# Normalization
NORMALIZATION_FIELD = 'normalization_field.nii'
NORMALIZATION_FIELD_INVERTED = 'normalization_field_inverted.nii'

# atlases
TALAIRACH = 'MNI Talairach Daemon Labels'
YEO = 'Yeo\'s Cortical Parcellation'
AAL = 'Automated Anatomical Labeling (AAL)'
