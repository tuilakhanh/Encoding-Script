import vapoursynth as vs
core = vs.core

import lvsfunc as lvf
import kagefunc as kgf
from vsutil import depth
from functools import partial

def hardsub(clip_a: vs.VideoNode, clip_b: vs.VideoNode) -> vs.VideoNode:
	mask = kgf.hardsubmask(clip_a, clip_b)
	clip = core.std.MaskedMerge(clip_b, clip_a, mask)
	return clip

def sign_text(clip_a: vs.VideoNode, clip_b: vs.VideoNode, signs = []) -> vs.VideoNode:
	mask_fade = lvf.util.quick_resample(
		clip_a, partial(kgf.hardsubmask_fades, ref=clip_b, expand_n=20, highpass=6000)
	)
	clip_signs = core.std.MaskedMerge(clip_b, clip_a, mask_fade)
	clip = lvf.rfs(clip_b, clip_signs, signs)
	return clip

def signs(clip_a: vs.VideoNode, clip_b: vs.VideoNode, signs = []) -> vs.VideoNode:
	mask_fade = lvf.util.quick_resample(
		clip_a, partial(kgf.hardsubmask_fades, ref=clip_b, expand_n=20, highpass=600)
	)
	clip_signs = core.std.MaskedMerge(clip_b, clip_a, mask_fade)
	clip = lvf.rfs(clip_b, clip_signs, signs)

def op_ed(clip_a: vs.VideoNode, clip_b: vs.VideoNode) -> vs.VideoNode:
	mask_fade = lvf.util.quick_resample(
		clip_a, partial(kgf.hardsubmask_fades, ref=clip_b, expand_n=10, highpass=20000)
	)
	clip = core.std.MaskedMerge(clip_b, clip_a, mask_fade)
	return clip

src_a = lvf.src(r'[VNFS] Steins;Gate 01 [BD][720p][v3].mkv')
src_a = depth(src_a, 32)
src_a = core.fmtc.resample(src_a, 1920, 1080, kernel = 'bilinear')
src_a = depth(src_a, 10)

src_b = lvf.src(r'[Beatrice-Raws] Steins;Gate [BDRip 1920x1080 x264 FLAC]\[Beatrice-Raws] Steins;Gate 01 [BDRip 1920x1080 x264 FLAC].mkv')

signs = [
(1549, 1669), (2310, 2389), (5367, 5390),
(9515, 9520), (13140, 13221), (18867, 19111),
(30993, 31122), (31256, 31344)
]

op_eds = [
(15202, 17370), (31910, 34452)
]

subtitles = hardsub(src_a, src_b)
sign_text = sign_text(src_a, subtitles, signs)

op = lvf.rfs(sign_text, op_ed(src_a, src_b), op_eds)


out = op
out.set_output()
