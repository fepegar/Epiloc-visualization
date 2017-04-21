import os
import epiloc_constants as const

MASK_ELECTRODES = 'electrodes.nii.gz'
MESH_ELECTRODES = 'electrodes.vtk'
LOG = '_log_postOp.txt'
TRAJECTORIES = 'trajectories.xml'
INVERSE_WARP = 'y_' #'invertedField_'  #'iy_r'
ANATOMICAL_LOCALIZATIONS = 'anatomical_localizations.csv'
ELECTRODES_OBJECT = 'electrodes.pkl'
FRAME_TO_CTPOST = '_frame_2_ctpost.xfm'
ELECTRODES_XML = 'electrodes.xml'
STATS = 'stats.pdf'
MESH_AC = 'landmark_ac'
MESH_PC = 'landmark_pc'
NORMALIZED_T1 = 'w'
IMA_T1MRI_POST = 't1mri_post.nii.gz'
REGIMA_T1MRIPOST2T1MRI = 't1mri_post_2_t1mri.nii.gz'
REGMAT_T1MRIPOST2ACPC = 't1mri_post_2_acpc.xfm'
REGMAT_T1MRIPOST2T1MRI = 't1mri_post_2_t1mri.xfm'
REGMAT_T1MRI2T1MRIPOST = 't1mri_2_t1mri_post.xfm'

class PatientModelEpilepsy:
  def __init__(self,patientId, epilepsyId=None, rootDir=None):

    self.patientId = patientId
    self.idString = str(patientId)
    self.epilepsyIdString = str(epilepsyId)
    self.rootDir = rootDir

    if rootDir is None:
      self.rootDir = 'patients'
    # ========================================== Directories ====================================================

    # root directory for the patient
    self.dataDir = os.path.join(self.rootDir,self.idString)

    # directory for the transformed images
    self.imagesDir = os.path.join(self.dataDir, 'nifti')

    # log and perf directories
    self.logDir = os.path.join(self.dataDir,'log')
    self.perfDir = os.path.join(self.dataDir,'perf')

    # log and performance dictionary files
    self.logInclusionPath = os.path.join(self.logDir,self.idString+'_log_inclusion.txt')
    self.logPreOpPath = os.path.join(self.logDir,self.idString+'_log_preop.txt')
    self.logPostOpPath = os.path.join(self.logDir,self.idString+'_log_postop.txt')
    self.logYebPath = os.path.join(self.logDir,self.idString+'_log_yeb.txt')
    self.perfInclusionPath = os.path.join(self.perfDir,self.idString+'_perf_inclusion.pkl')
    self.perfPreOpPath = os.path.join(self.perfDir,self.idString+'_perf_preop.pkl')
    self.perfPostOpPath = os.path.join(self.perfDir,self.idString+'_perf_postop.pkl')
    self.perfYebPath = os.path.join(self.perfDir,self.idString+'_perf_yeb.pkl')

    # directory for templates (locally copied in patients folder for portability reasons)
    self.templateDir = os.path.join(self.dataDir,'template')

    # masks
    self.maskDir = os.path.join(self.dataDir,'mask')
    self.maskMriRefDir = os.path.join(self.maskDir,'ref_t1mri')
    self.maskCtPostRefDir = os.path.join(self.maskDir,'ref_ctpost')
    self.maskCtPreRefDir = os.path.join(self.maskDir,'ref_ctpre')
    self.maskT1MriPreRefDir = os.path.join(self.maskDir,'ref_t1mripre')
    self.maskParkRefDir = os.path.join(self.maskDir,'ref_park')

    # masked images
    self.maskedDir = os.path.join(self.dataDir,'masked')

    # meshes
    self.meshDir = os.path.join(self.dataDir,'mesh')
    self.meshRASDir = self.meshDir
    self.meshLPSDir = os.path.join(self.dataDir,'mesh_itk')
    self.meshMriRefDir = os.path.join(self.meshRASDir,'ref_t1mri')
    self.meshCtPostRefDir = os.path.join(self.meshRASDir,'ref_ctpost')
    self.meshCtPreRefDir = os.path.join(self.meshRASDir,'ref_ctpre')
    self.meshParkRefDir = os.path.join(self.meshRASDir,'ref_park')
    self.meshT1MriPreRefDir = os.path.join(self.meshRASDir,'ref_t1mripre')
    self.meshParkAtlasDir = os.path.join(self.meshMriRefDir,'park_atlas')
    self.meshParkAtlasLinearDir = os.path.join(self.meshMriRefDir,'park_atlas_linear')
    self.meshYebAtlasDir = os.path.join(self.meshMriRefDir,'yeb_atlas')
    self.meshCtPostVoltageDir = os.path.join(self.meshCtPostRefDir,'voltage')

    self.meshElectrodesDir = os.path.join(self.meshCtPostRefDir,'electrodes')
    self.trajectoriesMeshesDir = os.path.join(self.meshCtPostRefDir,'trajectories')

    # registration
    self.regMatDir = os.path.join(self.dataDir,'reg_mat')
    self.regImaDir = os.path.join(self.dataDir,'reg_ima')

    # template registration pipeline
    self.parkPipelineDir = os.path.join(self.dataDir,'park_pipeline')
    self.atlasYEBPipelineDir = os.path.join(self.dataDir,'atlasyeb_pipeline')

    # slicer
    self.slicerSceneDir = os.path.join(self.dataDir,'slicer_scene')

    # color table
    self.colorTableDir = os.path.join(self.dataDir,'color_table')

    # mitk
    self.mitkDir = os.path.join(self.dataDir,'mitk')

    # trajectory
    self.trajectoryDir = os.path.join(self.dataDir,'trajectory')

    # trajectories
    self.trajectoriesDir = os.path.join(self.dataDir, 'trajectories')

    # normalization
    self.normalizationDir = os.path.join(self.dataDir,'normalization')

    # ========================================== Files ====================================================

    # log
    self.logPath = os.path.join(self.logDir, self.idString + LOG)

    # inclusion MRIs
    self.t1mriIncPath = os.path.join(self.dataDir,self.idString+'_'+const.IMA_T1MRI_INC)
    self.t2mriIncPath = os.path.join(self.dataDir,self.idString+'_'+const.IMA_T2MRI_INC)

    # pre-op MRIs (with frame)
    self.t1mriPrePath = os.path.join(self.imagesDir,self.idString+'_'+const.IMA_T1MRI_PRE)
    self.t2mriPrePath = os.path.join(self.imagesDir,self.idString+'_'+const.IMA_T2MRI_PRE)

    # for T2 Coro Interlaced Park Pitie
    self.t2mri1mmPrePath = os.path.join(self.dataDir,self.idString+'_'+const.IMA_T2MRI_1MM_PRE)
    self.t2mriInterlacedPrePath = os.path.join(self.dataDir,self.idString+'_'+const.IMA_T2MRI_INTERLACED_PRE)

    # MRIs of reference for segmentation: inclusion if they exist, otherwise pre-op
    self.refMriIsInclusion = None
    self.t2mriPath = os.path.join(self.dataDir,self.idString+'_'+const.IMA_T2MRI)
    self.t2mri1mmPath = os.path.join(self.dataDir,self.idString+'_'+const.IMA_T2MRI_1MM)
    self.t2mriInterlacedPath = os.path.join(self.dataDir,self.idString+'_'+const.IMA_T2MRI_INTERLACED)

    # CT pre- and post-op
    self.ctPrePath = os.path.join(self.dataDir,self.idString+'_'+const.IMA_CTPRE)
    self.ctPostPath = os.path.join(self.imagesDir,self.idString+'_'+const.IMA_CTPOST)

    # MRI post
    self.t1mriPostPath = os.path.join(self.imagesDir,self.idString+'_'+IMA_T1MRI_POST)

    # voltage images
    self.ctPostVoltageLeftPath = os.path.join(self.dataDir,self.idString+'_'+const.IMA_CTPOST_VOLTAGE_LEFT)
    self.ctPostVoltageRightPath = os.path.join(self.dataDir,self.idString+'_'+const.IMA_CTPOST_VOLTAGE_RIGHT)


    # registered images
    self.regImaT2Mri2T1MriPath = os.path.join(self.regImaDir,self.idString+'_'+const.REGIMA_T2MRI2T1MRI)
    self.regImaCtPre2T1MriPath = os.path.join(self.regImaDir,self.idString+'_'+const.REGIMA_CTPRE2T1MRI)
    self.regImaCtPost2CtPrePath = os.path.join(self.regImaDir,self.idString+'_'+const.REGIMA_CTPOST2CTPRE)
    self.regImaT1MriPost2T1MriPath = os.path.join(self.regImaDir,self.idString+'_'+REGIMA_T1MRIPOST2T1MRI)

    self.regImaInterlacedT2Mri2T1MriPath = os.path.join(self.regImaDir,self.idString+'_'+const.REGIMA_INTERLACEDT2MRI2T1MRI)


    self.regImaCtPost2T1MriPath = os.path.join(self.regImaDir,self.idString+'_'+const.REGIMA_CTPOST2T1MRI)

    # registration matrices FSL convention
    self.regMatFSLT2Mri2T1MriPath = os.path.join(self.regMatDir,self.idString+'_'+const.MAT_FSL+'_'+const.REGMAT_T2MRI2T1MRI)
    self.regMatFSLCtPre2T1MriPath = os.path.join(self.regMatDir,self.idString+'_'+const.MAT_FSL+'_'+const.REGMAT_CTPRE2T1MRI)
    self.regMatFSLCtPost2CtPrePath = os.path.join(self.regMatDir,self.idString+'_'+const.MAT_FSL+'_'+const.REGMAT_CTPOST2CTPRE)
    self.regMatFSLCtPost2T1MriPath = os.path.join(self.regMatDir,self.idString+'_'+const.MAT_FSL+'_'+const.REGMAT_CTPOST2T1MRI)
    self.regMatFSLT1MriPost2T1MriPath = os.path.join(self.regMatDir,self.idString+'_'+const.MAT_FSL+'_'+REGMAT_T1MRIPOST2T1MRI)
    self.regMatFSLT1Mri2T1MriPostPath = os.path.join(self.regMatDir,self.idString+'_'+const.MAT_FSL+'_'+REGMAT_T1MRI2T1MRIPOST)

    self.regMatFSLT1Mri2CtPrePath = os.path.join(self.regMatDir,self.idString+'_'+const.MAT_FSL+'_'+const.REGMAT_T1MRI2CTPRE)
    self.regMatFSLT1Mri2CtPostPath = os.path.join(self.regMatDir,self.idString+'_'+const.MAT_FSL+'_'+const.REGMAT_T1MRI2CTPOST)
    self.regMatFSLFrame2CtPreInitPath =  os.path.join(self.regMatDir,self.idString+'_'+const.MAT_FSL+'_'+const.REGMAT_FRAME2CTPRE_INIT)
    self.regMatFSLFrame2CtPrePath =  os.path.join(self.regMatDir,self.idString+'_'+const.MAT_FSL+'_'+const.REGMAT_FRAME2CTPRE)
    self.regMatFSLInterlacedT2Mri2T1MriPath = os.path.join(self.regMatDir,self.idString+'_'+const.MAT_FSL+'_'+const.REGMAT_INTERLACEDT2MRI2T1MRI)


    # registration matrices Nifti World To Nifti World

    # From T1
    self.regMatW2WT1Mri2CtPrePath = os.path.join(self.regMatDir,self.idString+'_'+const.MAT_WORLD2WORLD+'_'+const.REGMAT_T1MRI2CTPRE)
    self.regMatW2WT1Mri2T1MriPostPath = os.path.join(self.regMatDir,self.idString+'_'+const.MAT_WORLD2WORLD+'_'+REGMAT_T1MRI2T1MRIPOST)
    self.regMatW2WT1MriPost2T1MriPath = os.path.join(self.regMatDir,self.idString+'_'+const.MAT_WORLD2WORLD+'_'+REGMAT_T1MRIPOST2T1MRI)

    self.regMatW2WT1Mri2CtPostPath = os.path.join(self.regMatDir,self.idString+'_'+const.MAT_WORLD2WORLD+'_'+const.REGMAT_T1MRI2CTPOST)
    self.regMatW2WT1Mri2ParkPath = os.path.join(self.regMatDir,self.idString+'_'+const.MAT_WORLD2WORLD+'_'+const.REGMAT_T1MRI2PARK)
    self.regMatW2WT1Mri2ACPCPath = os.path.join(self.regMatDir,self.idString+'_'+const.MAT_WORLD2WORLD+'_'+const.REGMAT_T1MRI2ACPC)
    self.regMatW2WLHT1Mri2AtlasYEBPath = os.path.join(self.regMatDir,self.idString+'_'+const.MAT_WORLD2WORLD+'_'+const.REGMAT_T1MRI2YEB_LH)
    self.regMatW2WRHT1Mri2AtlasYEBPath = os.path.join(self.regMatDir,self.idString+'_'+const.MAT_WORLD2WORLD+'_'+const.REGMAT_T1MRI2YEB_RH)

    # From T2
    self.regMatW2WT2Mri2T1MriPath = os.path.join(self.regMatDir,self.idString+'_'+const.MAT_WORLD2WORLD+'_'+const.REGMAT_T2MRI2T1MRI)
    self.regMatW2WT2Mri2ParkPath = os.path.join(self.regMatDir,self.idString+'_'+const.MAT_WORLD2WORLD+'_'+const.REGMAT_T2MRI2PARK)
    self.regMatW2WT2Mri2ACPCPath = os.path.join(self.regMatDir,self.idString+'_'+const.MAT_WORLD2WORLD+'_'+const.REGMAT_T2MRI2ACPC)
    self.regMatW2WInterlacedT2Mri2T1MriPath = os.path.join(self.regMatDir,self.idString+'_'+const.MAT_WORLD2WORLD+'_'+const.REGMAT_INTERLACEDT2MRI2T1MRI)
    self.regMatW2WInterlacedT2Mri2ACPCPath = os.path.join(self.regMatDir,self.idString+'_'+const.MAT_WORLD2WORLD+'_'+const.REGMAT_INTERLACEDT2MRI2ACPC)

    # From CT-PRE
    self.regMatW2WCtPre2T1MriPath = os.path.join(self.regMatDir,self.idString+'_'+const.MAT_WORLD2WORLD+'_'+const.REGMAT_CTPRE2T1MRI)
    self.regMatW2WCtPre2ACPCPath = os.path.join(self.regMatDir,self.idString+'_'+const.MAT_WORLD2WORLD+'_'+const.REGMAT_CTPRE2ACPC)

    # From CT-POST
    self.regMatW2WCtPost2ParkPath = os.path.join(self.regMatDir,self.idString+'_'+const.MAT_WORLD2WORLD+'_'+const.REGMAT_CTPOST2PARK)
    self.regMatW2WCtPost2CtPrePath = os.path.join(self.regMatDir,self.idString+'_'+const.MAT_WORLD2WORLD+'_'+const.REGMAT_CTPOST2CTPRE)
    self.regMatW2WCtPost2T1MriPath = os.path.join(self.regMatDir,self.idString+'_'+const.MAT_WORLD2WORLD+'_'+const.REGMAT_CTPOST2T1MRI)
    self.regMatW2WCtPost2ACPCPath = os.path.join(self.regMatDir,self.idString+'_'+const.MAT_WORLD2WORLD+'_'+const.REGMAT_CTPOST2ACPC)
    self.regMatW2WT1MriPost2ACPCPath = os.path.join(self.regMatDir,self.idString+'_'+const.MAT_WORLD2WORLD+'_'+REGMAT_T1MRIPOST2ACPC)

    # From Frame
    self.regMatW2WFrame2CtPreInitPath =  os.path.join(self.regMatDir,self.idString+'_'+const.MAT_WORLD2WORLD+'_'+const.REGMAT_FRAME2CTPRE_INIT)
    self.regMatW2WFrame2CtPrePath =  os.path.join(self.regMatDir,self.idString+'_'+const.MAT_WORLD2WORLD+'_'+const.REGMAT_FRAME2CTPRE)
    self.regMatW2WFrame2ACPCPath =  os.path.join(self.regMatDir,self.idString+'_'+const.MAT_WORLD2WORLD+'_'+const.REGMAT_FRAME2ACPC)
    self.regMatW2WFrame2T1MriPrePath =  os.path.join(self.regMatDir,self.idString+'_'+const.MAT_WORLD2WORLD+'_'+const.REGMAT_FRAME2T1MRIPRE)

    # From Parkinson tempate
    self.regMatW2WPark2T1MriPath = os.path.join(self.regMatDir,self.idString+'_'+const.MAT_WORLD2WORLD+'_'+const.REGMAT_PARK2T1MRI)

    # From Atlas Yeb
    self.regMatW2WAtlasYEB2LHT1MriPath = os.path.join(self.regMatDir,self.idString+'_'+const.MAT_WORLD2WORLD+'_'+const.REGMAT_YEB2T1MRI_LH)
    self.regMatW2WAtlasYEB2RHT1MriPath = os.path.join(self.regMatDir,self.idString+'_'+const.MAT_WORLD2WORLD+'_'+const.REGMAT_YEB2T1MRI_RH)

    # registration matrices Slicer convention
    self.regMatSlicerT1Mri2ACPCPath = os.path.join(self.regMatDir,self.idString+'_'+const.MAT_SLICER+'_'+const.REGMAT_T1MRI2ACPC.replace('.xfm','.tfm'))
    self.regMatSlicerT2Mri2ACPCPath = os.path.join(self.regMatDir,self.idString+'_'+const.MAT_SLICER+'_'+const.REGMAT_T2MRI2ACPC.replace('.xfm','.tfm'))
    self.regMatSlicerInterlacedT2Mri2ACPCPath = os.path.join(self.regMatDir,self.idString+'_'+const.MAT_SLICER+'_'+const.REGMAT_INTERLACEDT2MRI2ACPC.replace('.xfm','.tfm'))
    self.regMatSlicerCtPre2ACPCPath = os.path.join(self.regMatDir,self.idString+'_'+const.MAT_SLICER+'_'+const.REGMAT_CTPRE2ACPC.replace('.xfm','.tfm'))
    self.regMatSlicerCtPost2ACPCPath = os.path.join(self.regMatDir,self.idString+'_'+const.MAT_SLICER+'_'+const.REGMAT_CTPOST2ACPC.replace('.xfm','.tfm'))
    self.regMatSlicerFrame2ACPCPath = os.path.join(self.regMatDir,self.idString+'_'+const.MAT_SLICER+'_'+const.REGMAT_FRAME2ACPC.replace('.xfm','.tfm'))
    self.regMatSlicerPark2ACPCPath = os.path.join(self.regMatDir,self.idString+'_'+const.MAT_SLICER+'_'+const.REGMAT_PARK2ACPC.replace('.xfm','.tfm'))
    self.regMatSlicerAtlasYEB2LHT1MriPath = os.path.join(self.regMatDir,self.idString+'_'+const.MAT_SLICER+'_'+const.REGMAT_YEB2T1MRI_LH.replace('.xfm','.tfm'))
    self.regMatSlicerAtlasYEB2RHT1MriPath = os.path.join(self.regMatDir,self.idString+'_'+const.MAT_SLICER+'_'+const.REGMAT_YEB2T1MRI_RH.replace('.xfm','.tfm'))
    self.regMatW2WFrame2CtPostPath = os.path.join(self.regMatDir,self.idString+'_'+const.MAT_WORLD2WORLD+FRAME_TO_CTPOST)
    self.regMatSlicerT1MriPost2ACPCPath = os.path.join(self.regMatDir,self.idString+'_'+const.MAT_SLICER+'_'+REGMAT_T1MRIPOST2ACPC.replace('.xfm','.tfm'))


    # masks in T1MRI referential
    self.maskHeadPath = os.path.join(self.maskMriRefDir,self.idString+'_'+const.MASK_HEAD)
    self.maskBrainPath = os.path.join(self.maskMriRefDir,self.idString+'_'+const.MASK_BRAIN)
    self.maskWMPath = os.path.join(self.maskMriRefDir,self.idString+'_'+const.MASK_WM)
    self.maskGMPath = os.path.join(self.maskMriRefDir,self.idString+'_'+const.MASK_GM)
    self.maskCSFPath = os.path.join(self.maskMriRefDir,self.idString+'_'+const.MASK_CSF)
    self.maskCortexLeftPath = os.path.join(self.maskMriRefDir,self.idString+'_'+const.MASK_CORTEX_LEFT)
    self.maskCortexRightPath = os.path.join(self.maskMriRefDir,self.idString+'_'+const.MASK_CORTEX_RIGHT)
    self.maskSkinPath = os.path.join(self.maskMriRefDir,self.idString+'_'+const.MASK_SKIN)
    self.maskSkinEdgesPath = os.path.join(self.maskMriRefDir,self.idString+'_'+const.MASK_SKIN_EDGES)
    self.maskParkAtlasPath = os.path.join(self.maskMriRefDir,self.idString+'_'+const.MASK_PARKINSON_ATLAS)
    self.maskParkAtlasLinearPath = os.path.join(self.maskMriRefDir,self.idString+'_'+const.MASK_PARKINSON_ATLAS_LINEAR)

    self.maskElectrodeLeftPath = os.path.join(self.maskMriRefDir,self.idString+'_'+const.MASK_ELECTRODE_LEFT)
    self.maskElectrodeRightPath = os.path.join(self.maskMriRefDir,self.idString+'_'+const.MASK_ELECTRODE_RIGHT)


    # masks in T1Mri-PRE referential
    self.t1mriPreRefMaskFrameArtifactPath = os.path.join(self.maskT1MriPreRefDir,self.idString+'_'+const.REF_T1MRIPRE+'_'+const.MASK_FRAME_ARTIFACT)

    # masks in CT-PRE referential
    self.ctPreRefMaskFrameArtifactLeftPath = os.path.join(self.maskCtPreRefDir,self.idString+'_'+const.REF_CTPRE+'_'+const.MASK_FRAME_ARTIFACT_LEFT)
    self.ctPreRefMaskFrameArtifactRightPath = os.path.join(self.maskCtPreRefDir,self.idString+'_'+const.REF_CTPRE+'_'+const.MASK_FRAME_ARTIFACT_RIGHT)
    self.ctPreRefMaskFrameArtifactAnteriorPath = os.path.join(self.maskCtPreRefDir,self.idString+'_'+const.REF_CTPRE+'_'+const.MASK_FRAME_ARTIFACT_ANTERIOR)
    self.ctPreRefMaskFrameArtifactPath = os.path.join(self.maskCtPreRefDir,self.idString+'_'+const.REF_CTPRE+'_'+const.MASK_FRAME_ARTIFACT)
    self.ctPreRefMaskFrameArtifactCCPath = os.path.join(self.maskCtPreRefDir,self.idString+'_'+const.REF_CTPRE+'_'+const.MASK_FRAME_ARTIFACT_CC)
    self.ctPreRefMaskFrameModelPath = os.path.join(self.maskCtPreRefDir,self.idString+'_'+const.REF_CTPRE+'_'+const.MASK_FRAME_MODEL)
    self.ctPreRefMaskSkullPath = os.path.join(self.maskCtPreRefDir,self.idString+'_'+const.REF_CTPRE+'_'+const.MASK_SKULL)
    self.ctPreRefMaskSupportsPath = os.path.join(self.maskCtPreRefDir,self.idString+'_'+const.REF_CTPRE+'_'+const.MASK_SUPPORTS)
    self.ctPreRefMaskBrainPath = os.path.join(self.maskCtPreRefDir,self.idString+'_'+const.REF_CTPRE+'_'+const.MASK_BRAIN)

    # masks in CT-POST referential
    self.ctPostRefMaskSkullPath = os.path.join(self.maskCtPostRefDir,self.idString+'_'+const.REF_CTPOST+'_'+const.MASK_SKULL)
    self.ctPostRefMaskCortexLeftPath = os.path.join(self.maskCtPostRefDir,self.idString+'_'+const.REF_CTPOST+'_'+const.MASK_CORTEX_LEFT)
    self.ctPostRefMaskCortexRightPath = os.path.join(self.maskCtPostRefDir,self.idString+'_'+const.REF_CTPOST+'_'+const.MASK_CORTEX_RIGHT)
    self.ctPostRefMaskElectrodeLeftPath = os.path.join(self.maskCtPostRefDir,self.idString+'_'+const.REF_CTPOST+'_'+const.MASK_ELECTRODE_LEFT)
    self.ctPostRefMaskElectrodeRightPath = os.path.join(self.maskCtPostRefDir,self.idString+'_'+const.REF_CTPOST+'_'+const.MASK_ELECTRODE_RIGHT)

    # CT-POST voltage masks
    self.ctPostRefMaskVoltageLeftPath = os.path.join(self.maskCtPostRefDir,self.idString+'_'+const.REF_CTPOST+'_'+const.MASK_VOLTAGE_LEFT)
    self.ctPostRefMaskVoltageRightPath = os.path.join(self.maskCtPostRefDir,self.idString+'_'+const.REF_CTPOST+'_'+const.MASK_VOLTAGE_RIGHT)
    self.ctPostRefMaskVoltagePath = os.path.join(self.maskCtPostRefDir,self.idString+'_'+const.REF_CTPOST+'_'+const.MASK_VOLTAGE)

    # meshes for visualization in MITK
    self.MITKmeshSulciPath = os.path.join(self.mitkDir,self.idString+'_'+const.MESH_SULCI)
    self.MITKmeshHeadPath = os.path.join(self.mitkDir,self.idString+'_'+const.MESH_HEAD)
    self.MITKmeshInsertionZoneLeftPath = os.path.join(self.mitkDir,self.idString+'_'+const.MESH_INSERTION_ZONE_LEFT)
    self.MITKmeshInsertionZoneRightPath = os.path.join(self.mitkDir,self.idString+'_'+const.MESH_INSERTION_ZONE_RIGHT)

    # meshes in MRI referential
    self.meshSulciLeftPath = os.path.join(self.meshMriRefDir,self.idString+'_'+const.MESH_SULCI_LEFT)
    self.meshSulciRightPath = os.path.join(self.meshMriRefDir,self.idString+'_'+const.MESH_SULCI_RIGHT)

    self.meshHeadPath = os.path.join(self.meshMriRefDir,self.idString+'_'+const.MESH_HEAD)
    self.meshSkinPath = os.path.join(self.meshMriRefDir,self.idString+'_'+const.MESH_SKIN)
    self.meshSkinEdgesPath = os.path.join(self.meshMriRefDir,self.idString+'_'+const.MESH_SKIN_EDGES)

    self.meshGrayPialLeftPath = os.path.join(self.meshMriRefDir,self.idString+'_'+const.MESH_GRAY_PIAL_LEFT)
    self.meshGrayPialRightPath = os.path.join(self.meshMriRefDir,self.idString+'_'+const.MESH_GRAY_PIAL_RIGHT)

    self.meshGrayWhiteLeftPath = os.path.join(self.meshMriRefDir,self.idString+'_'+const.MESH_GRAY_WHITE_LEFT)
    self.meshGrayWhiteRightPath = os.path.join(self.meshMriRefDir,self.idString+'_'+const.MESH_GRAY_WHITE_RIGHT)

    self.meshACPath = os.path.join(self.meshMriRefDir,self.idString+'_'+const.MESH_AC)
    self.meshPCPath = os.path.join(self.meshMriRefDir,self.idString+'_'+const.MESH_PC)
    self.meshIHPath = os.path.join(self.meshMriRefDir,self.idString+'_'+const.MESH_IH)

    self.meshInsertionZoneLeftPath = os.path.join(self.meshMriRefDir,self.idString+'_'+const.MESH_INSERTION_ZONE_LEFT)
    self.meshInsertionZoneRightPath = os.path.join(self.meshMriRefDir,self.idString+'_'+const.MESH_INSERTION_ZONE_RIGHT)

    # meshes in T1Mri-PRE referential
    self.t1mriPreRefMeshFrameArtifactPath = os.path.join(self.meshT1MriPreRefDir,self.idString+'_'+const.REF_T1MRIPRE+'_'+const.MESH_FRAME_ARTIFACT)
    self.t1mriPreRefMeshFrameModelPath = os.path.join(self.meshT1MriPreRefDir,self.idString+'_'+const.REF_T1MRIPRE+'_'+const.MESH_FRAME_MODEL)

    # meshes in CT-PRE referential
    self.ctPreRefMeshFrameArtifactPath = os.path.join(self.meshCtPreRefDir,self.idString+'_'+const.REF_CTPRE+'_'+const.MESH_FRAME_ARTIFACT)
    self.ctPreRefMeshFramePointsPath = os.path.join(self.meshCtPreRefDir,self.idString+'_'+const.REF_CTPRE+'_'+const.MESH_FRAME_POINTS)
    self.ctPreRefMeshFrameModelPath = os.path.join(self.meshCtPreRefDir,self.idString+'_'+const.REF_CTPRE+'_'+const.MESH_FRAME_MODEL)
    self.ctPreRefMeshSkullPath = os.path.join(self.meshCtPreRefDir,self.idString+'_'+const.REF_CTPRE+'_'+const.MESH_SKULL)
    self.ctPreRefMeshSupportsPath = os.path.join(self.meshCtPreRefDir,self.idString+'_'+const.REF_CTPRE+'_'+const.MESH_SUPPORTS)

    # meshes in CT POST referential
    self.ctPostRefMeshElectrodeLeftPath = os.path.join(self.meshCtPostRefDir,self.idString+'_'+const.REF_CTPOST+'_'+const.MESH_ELECTRODE_LEFT)
    self.ctPostRefMeshElectrodeRightPath = os.path.join(self.meshCtPostRefDir,self.idString+'_'+const.REF_CTPOST+'_'+const.MESH_ELECTRODE_RIGHT)
    self.ctPostRefMeshElectrodeModelLeftAxisPath = os.path.join(self.meshCtPostRefDir,self.idString+'_'+const.REF_CTPOST+'_'+const.MESH_ELECTRODE_MODEL_AXIS_LEFT)
    self.ctPostRefMeshElectrodeModelLeftContactsPath = os.path.join(self.meshCtPostRefDir,self.idString+'_'+const.REF_CTPOST+'_'+const.MESH_ELECTRODE_MODEL_CONTACTS_LEFT)
    self.ctPostRefMeshElectrodeModelRightAxisPath = os.path.join(self.meshCtPostRefDir,self.idString+'_'+const.REF_CTPOST+'_'+const.MESH_ELECTRODE_MODEL_AXIS_RIGHT)
    self.ctPostRefMeshElectrodeModelRightContactsPath = os.path.join(self.meshCtPostRefDir,self.idString+'_'+const.REF_CTPOST+'_'+const.MESH_ELECTRODE_MODEL_CONTACTS_RIGHT)
    self.ctPostRefMeshElectrodeCurveLeftPath = os.path.join(self.meshCtPostRefDir,self.idString+'_'+const.REF_CTPOST+'_'+const.BAR_MESH_ELECTRODE_LEFT)
    self.ctPostRefMeshElectrodeCurveRightPath = os.path.join(self.meshCtPostRefDir,self.idString+'_'+const.REF_CTPOST+'_'+const.BAR_MESH_ELECTRODE_RIGHT)

    # meshes in Parkinson Template referential
    self.parkRefMeshElectrodeLeftPath = os.path.join(self.meshParkRefDir,self.idString+'_'+const.REF_PARK+'_'+const.MESH_ELECTRODE_LEFT)
    self.parkRefMeshElectrodeRightPath = os.path.join(self.meshParkRefDir,self.idString+'_'+const.REF_PARK+'_'+const.MESH_ELECTRODE_RIGHT)
    self.parkRefMeshElectrodeModelLeftAxisPath = os.path.join(self.meshParkRefDir,self.idString+'_'+const.REF_PARK+'_'+const.MESH_ELECTRODE_MODEL_AXIS_LEFT)
    self.parkRefMeshElectrodeModelLeftContactsPath = os.path.join(self.meshParkRefDir,self.idString+'_'+const.REF_PARK+'_'+const.MESH_ELECTRODE_MODEL_CONTACTS_LEFT)
    self.parkRefMeshElectrodeModelRightAxisPath = os.path.join(self.meshParkRefDir,self.idString+'_'+const.REF_PARK+'_'+const.MESH_ELECTRODE_MODEL_AXIS_RIGHT)
    self.parkRefMeshElectrodeModelRightContactsPath = os.path.join(self.meshParkRefDir,self.idString+'_'+const.REF_PARK+'_'+const.MESH_ELECTRODE_MODEL_CONTACTS_RIGHT)

    # masked images
    self.maskedT1mriBrainPath = os.path.join(self.maskedDir,self.idString+'_'+const.MASKED_T1MRI_BRAIN)
    self.maskedT1MriHeadPath = os.path.join(self.maskedDir,self.idString+'_'+const.MASKED_T1MRI_HEAD)
    self.maskedCtPostCortexLeftPath = os.path.join(self.maskedDir,self.idString+'_'+const.MASKED_CTPOST_CORTEX_LEFT)
    self.maskedCtPostCortexRightPath = os.path.join(self.maskedDir,self.idString+'_'+const.MASKED_CTPOST_CORTEX_RIGHT)

    # MRML scenes
    self.sceneInclusionPath = os.path.join(self.slicerSceneDir,self.idString+'_'+const.MRML_SCENE_INCLUSION)
    self.MITKsceneInclusionPath = os.path.join(self.mitkDir,self.idString+'_'+const.MRML_SCENE_INCLUSION)
    self.scenePreOpPath = os.path.join(self.slicerSceneDir,self.idString+'_'+const.MRML_SCENE_PREOP)
    self.scenePreOpPitiePath = os.path.join(self.slicerSceneDir,self.idString+'_'+const.MRML_SCENE_PREOP_PITIE)
    self.scenePreOpElectrodeLeftPath = os.path.join(self.slicerSceneDir,self.idString+'_'+const.MRML_SCENE_PREOP_ELECTRODE_LEFT)
    self.scenePreOpElectrodeRightPath = os.path.join(self.slicerSceneDir,self.idString+'_'+const.MRML_SCENE_PREOP_ELECTRODE_RIGHT)
    self.scenePostOpPath = os.path.join(self.slicerSceneDir,self.idString+'_'+const.MRML_SCENE_POSTOP)
    self.scenePostOpElectrodeLeftPath = os.path.join(self.slicerSceneDir,self.idString+'_'+const.MRML_SCENE_POSTOP_ELECTRODE_LEFT)
    self.scenePostOpElectrodeRightPath = os.path.join(self.slicerSceneDir,self.idString+'_'+const.MRML_SCENE_POSTOP_ELECTRODE_RIGHT)
    self.scenePostOpVoltagePath = os.path.join(self.slicerSceneDir,self.idString+'_'+const.MRML_SCENE_POSTOP_VOLTAGE)
    self.sceneYeBPath = os.path.join(self.slicerSceneDir,self.idString+'_'+const.MRML_SCENE_YEB)

    # color tables
    self.parkinsonColorTablePath = os.path.join(self.colorTableDir,self.idString+'_'+const.PARK_COLOR_TABLE)
    self.voltageColorTablePath = os.path.join(self.colorTableDir,self.idString+'_'+const.VOLTAGE_COLOR_TABLE)
    self.yebColorTablePath = os.path.join(self.colorTableDir,self.idString+'_'+const.YEB_COLOR_TABLE)

    # clinical template volume
    self.clinicalNoCriteriaVolumePath = os.path.join(self.templateDir,'clinical_atlas.nii.gz')

    # trajectories
    self.inclusionTrajectoryManualPath = os.path.join(self.trajectoryDir,self.idString+'_'+const.INCLUSION_TRAJECTORY_MANUAL)
    self.inclusionTrajectoryAutomaticPath = os.path.join(self.trajectoryDir,self.idString+'_'+const.INCLUSION_TRAJECTORY_AUTOMATIC)
    self.leksellTrajectoryPath = os.path.join(self.trajectoryDir,self.idString+'_'+const.LEKSELL_TRAJECTORY)


    # intialise reference MRI
    if os.path.exists(self.t1mriIncPath):
      self.refMriIsInclusion = True
    else:
      self.refMriIsInclusion = False

    if os.path.exists(self.t2mriPath):
      self.t2MriPresent = True
    else:
      self.t2MriPresent = False

    if os.path.exists(self.t2mri1mmPath):
      self.t2Mri1mmPresent = True
    else:
      self.t2Mri1mmPresent = False

    # Normalization
    self.inverseDeformationFieldPath  = os.path.join(self.normalizationDir, INVERSE_WARP  + self.idString+'_'+const.MASKED_T1MRI_HEAD).rstrip('.gz')
    self.normalizedT1MriPath          = os.path.join(self.normalizationDir, NORMALIZED_T1 + self.idString+'_'+const.MASKED_T1MRI_HEAD).rstrip('.gz')
    self.maskedHeadUnbiasedPath = os.path.join(self.maskedDir, self.idString+'_'+const.MASKED_T1MRI_HEAD_UNBIASED)
    self.normalizationFieldPath = os.path.join(self.normalizationDir, self.idString+'_'+const.NORMALIZATION_FIELD)
    self.normalizationFieldInvertedPath = os.path.join(self.normalizationDir, self.idString+'_'+const.NORMALIZATION_FIELD_INVERTED)
    self.regImaCtPost2MNIPath = os.path.join(self.normalizationDir, 'w' + self.idString+'_'+const.REGIMA_CTPOST2T1MRI).rstrip('.gz')
    self.regImaT1MriPost2MNIPath = os.path.join(self.normalizationDir, 'w' + self.idString+'_'+REGIMA_T1MRIPOST2T1MRI).rstrip('.gz')
    self.regImaT1MriPre2MNIPath = os.path.join(self.normalizationDir, 'w' + self.idString+'_'+const.IMA_T1MRI_PRE).rstrip('.gz')
    self.mniRefMaskHeadPath = os.path.join(self.normalizationDir, 'w' + self.idString+'_'+const.MASK_HEAD)


    self.localizationsPath = os.path.join(self.dataDir, self.idString+'_'+ANATOMICAL_LOCALIZATIONS)

    # masks in CT-POST referential
    self.ctPostRefMaskElectrodesPath = os.path.join(self.maskCtPostRefDir, self.idString+'_'+const.REF_CTPOST+'_'+MASK_ELECTRODES)

    # meshes
    self.meshShaftsPath = os.path.join(self.meshElectrodesDir, self.idString+'_shafts.vtk')
    self.meshScrewsPath = os.path.join(self.meshElectrodesDir, self.idString+'_screws.vtk')

    # meshes in CT POST referential
    self.ctPostRefMeshElectrodesPath = os.path.join(self.meshCtPostRefDir, self.idString+'_'+const.REF_CTPOST+'_'+MESH_ELECTRODES)
    self.meshACFramePath = os.path.join(self.meshCtPostRefDir, self.idString+'_'+const.REF_CTPOST+MESH_AC+'_frame.vtk')
    self.meshPCFramePath = os.path.join(self.meshCtPostRefDir, self.idString+'_'+const.REF_CTPOST+MESH_PC+'_frame.vtk')

    # MRML scene
    self.scenePath = os.path.join(self.slicerSceneDir,self.idString+'_'+const.MRML_SCENE_POSTOP)
    self.sceneMNIPath = os.path.join(self.slicerSceneDir,self.idString+'_'+const.MRML_SCENE_MNI)

    # trajectories information
    self.trajectoriesPath = os.path.join(self.trajectoriesDir, self.idString+'_'+TRAJECTORIES)

    self.electrodesPath = os.path.join(self.dataDir, self.idString+'_'+ELECTRODES_OBJECT)
    self.labeledDir = os.path.join(self.maskCtPostRefDir, 'labeled')

    self.ctPostRefMaskHeadPath = os.path.join(self.maskCtPostRefDir, self.idString+'_'+const.REF_CTPOST+'_'+const.MASK_HEAD)
    self.labeledElectrodesPath = os.path.join(self.labeledDir, self.idString+'_labeledElectrodes.nii.gz')

    # results
    self.coordinatesPath = os.path.join(self.dataDir, self.idString+'_'+ANATOMICAL_LOCALIZATIONS)

    self.xmlPath = os.path.join(self.dataDir, self.idString+'_'+ELECTRODES_XML)
    self.xmlVerifiedPath = self.xmlPath.replace('.xml', '_verified.xml')

    self.statsPath = os.path.join(self.dataDir, self.idString+'_' + STATS)

    self.templatesDir = os.path.join(self.dataDir, 'templates')
    self.templateDartelPath = os.path.join(self.templatesDir, 'avgT1_Dartel_IXI550_MNI152.nii')
    self.templatePath = os.path.join(self.templatesDir, 'T1.nii')



