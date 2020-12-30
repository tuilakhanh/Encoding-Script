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

src_a = lvf.src(r'[VNFS] Steins;Gate 07 [BD][720p][v3].mkv')
src_a = depth(src_a, 32)
src_a = core.fmtc.resample(src_a, 1920, 1080, kernel = 'bilinear')
src_a = depth(src_a, 10)

src_b = lvf.src(r'[Beatrice-Raws] Steins;Gate [BDRip 1920x1080 x264 FLAC]\[Beatrice-Raws] Steins;Gate 07 [BDRip 1920x1080 x264 FLAC].mkv')

signs = [
(2592, 2625), (4939, 5058), (6178, 6200), 
(8960, 9009), (11851, 11895), (13680, 13761),
(15345, 15403), (26531, 26590), (26707, 26759),
(30349, 30412)
]

op_eds = [
(2782, 4877), (31895, 34652)
]

subtitles = hardsub(src_a, src_b)
sign_text = sign_text(src_a, subtitles, signs)

op = lvf.rfs(sign_text, op_ed(src_a, src_b), op_eds)


out = op#lvf.comparison.compare(subtitles, src_b)#), [3154]
#subtitles_op_ed[2782:4938]
out.set_output()
