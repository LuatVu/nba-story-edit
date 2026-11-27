"""Hand tags (groups only) for templates that have no CURATED entry, keyed by index id.
Written from the template name + common meme knowledge, 27/11/2026. Format: "id:group group".
Groups 'blank' (empty canvas / generic format) and 'nba_sports' (real NBA/sports people) are extra.
"""
EXTRA_CATS = {
    "blank": ("blank template empty canvas generic format", "trống mẫu trắng khung trống"),
    # Only explicit words: "cầu thủ"/"player" appear in almost every prompt and must not pull everything here.
    "nba_sports": ("lebron shaq adam silver schefter shannon sharpe ronaldo real athlete meme sports meme",
                   "meme người thật thể thao meme vận động viên"),
}

RAW = """
12:victory mock|65:confused|100:versus power|124:explain smart_idea|125:explain streak_fail|126:blank|130:rejection lonely_sad|142:fear_panic awkward
150:power praise_great|154:secret_smug chaos_evil|157:argument scream_hype|162:chain_reaction levels|165:argument|166:then_vs_now|167:power|169:laugh mock
171:mock|176:thinking smart_idea|181:backfire|190:money_pay|198:explain|201:levels backfire|207:fear_panic hidden_pain|208:shock|211:explain
223:protect|232:secret_smug|233:clown fancy|249:shock|257:shock awkward|258:mock|261:blank|265:laugh|266:versus|267:clown|268:temptation
275:victory|285:thinking|293:neglect|294:protect alliance|307:denial|311:begging|312:explain power|313:secret_smug|320:same pointing|321:power victory
322:fear_panic|323:fancy|327:money_pay|329:money_pay|336:secret_smug|337:mock confused|342:sleep_bored|343:explain|344:chaos_evil|348:fear_panic scream_hype
352:argument|354:lonely_sad|359:explain|362:blank|364:confused|369:argument|372:confused|376:begging|379:squad alliance|384:explain|388:backfire
394:versus same|395:temptation|396:chaos_evil secret_smug|398:explain then_vs_now|399:explain smart_idea|405:smart_idea|410:begging|413:choice|414:loss_regret|420:fear_panic
422:levels boardroom|423:confused|424:power|426:then_vs_now levels|428:explain|429:lonely_sad|430:victory|431:confused|432:protect hard_task|434:weak lonely_sad
435:streak_fail explain|437:disappointed shock|439:victory|441:power levels|442:reveal|443:versus|444:disappointed|445:then_vs_now|446:same pointing|448:awkward
449:versus then_vs_now|452:victory squad|453:begging choice|455:explain|456:loss_regret|458:smart_idea|459:thinking|460:hidden_pain|464:explain|466:bad_luck
467:streak_fail|468:fear_panic|470:choice|472:lonely_sad envy_outsider|473:power|476:argument|477:then_vs_now|478:lonely_sad doom|479:argument|480:reaction
481:waiting nostalgia|482:victory|483:fear_panic doom|485:choice|487:reveal|489:victory|490:fear_panic|491:begging|494:sleep_bored|495:explain
496:victory scream_hype|498:explain|500:clown|501:same versus|502:versus|503:same|505:scream_hype chaos_evil|506:explain|508:smart_idea|509:begging
510:confused|511:versus|514:confused|515:protect|516:awkward|517:explain|518:shock|519:everywhere|521:victory|522:smart_idea|523:fancy versus
524:backfire|528:reveal|530:everywhere|532:chaos_evil|534:thinking|538:power|539:rejection|540:argument scream_hype|543:backfire|545:same|546:alliance
547:power doom|548:then_vs_now|550:chaos_evil secret_smug|551:levels|552:same versus|553:reaction|554:power victory|555:hidden_pain|557:protect|558:explain
561:explain|562:praise_great|563:victory|564:argument|567:smart_idea|569:power|570:smart_idea|571:then_vs_now|572:confused|577:alliance|578:power
579:excuse smart_idea|580:fear_panic|582:rejection|583:victory mock|586:confused|587:fear_panic|588:chaos_evil|591:temptation|592:secret_smug|593:lonely_sad
594:doom chaos_evil|595:choice|598:shock|599:levels|600:levels|602:fancy|604:same|607:protect|608:blank|612:levels|614:shock|615:power doom
616:chaos_evil|617:confused|619:doom|621:mock|624:awkward|627:temptation|630:fancy|631:disappointed|632:secret_smug|633:power|634:victory
636:clown smart_idea|638:rejection power|641:awkward|643:argument|647:victory|649:reveal|650:weak|653:argument|655:confused|656:begging|658:confused
659:squad|661:same|664:confused|666:shock|668:then_vs_now|669:confused versus|673:confused|674:argument|675:secret_smug reveal|676:levels|678:doom
679:mock|681:blank|684:disappointed|685:versus|686:switch_betray|690:rejection|692:alliance squad|694:fear_panic|695:alliance|696:streak_fail|700:shock money_pay
702:fancy|705:blank|706:slap_correct|707:smart_idea|708:chain_reaction|709:fear_panic|711:awkward|712:explain|714:disappointed|715:choice|716:confused argument
718:chaos_evil|719:secret_smug|720:switch_betray disappointed|723:backfire levels|725:smart_idea|730:levels|732:rejection|734:victory|735:victory|736:explain
737:rejection|740:disappointed|741:explain|742:victory|744:blank|745:explain|746:clown|748:victory|749:shock|750:backfire|751:argument|752:begging
753:explain|754:secret_smug|756:chaos_evil doom|757:fear_panic|758:explain|759:doom|760:secret_smug|761:squad|764:explain|766:explain|767:explain
769:explain|771:power|780:explain|782:choice|785:confused|786:explain|787:squad|789:confused|794:power|797:argument|798:reaction|799:confused|801:shock
802:backfire|803:squad|804:protect|805:money_pay|808:nba_sports trade_deal explain|809:doom power|810:begging|811:argument|812:reveal confused|813:waiting
814:chaos_evil|819:power|820:rejection|821:praise_great|822:power levels|823:reveal|826:begging|827:power|828:reaction|829:chaos_evil versus|830:fancy
831:disappointed|834:fear_panic protect|835:power|836:explain|838:argument versus|840:power versus|841:secret_smug|843:protect|844:reaction|845:secret_smug
846:secret_smug|847:fancy|849:explain|851:scream_hype|852:debate|855:disappointed|856:fancy|858:chaos_evil|859:victory|861:confused|862:power
864:argument disappointed|865:scream_hype|866:lonely_sad|868:lonely_sad|869:then_vs_now|870:lonely_sad|871:fear_panic|872:explain|875:fear_panic
877:secret_smug|878:explain|879:begging|880:blank|881:protect|882:power|884:choice|886:secret_smug|887:blank|888:argument|889:levels|892:fancy
894:sleep_bored|895:victory|897:awkward|900:smart_idea|901:levels|902:stubborn|903:power|905:argument|906:explain|908:fear_panic|911:victory
912:victory|913:clown|914:nba_sports explain|915:rejection|916:begging|917:alliance|921:victory|922:mock|926:neglect|927:secret_smug|928:mock
929:power|932:temptation|933:mock|934:nostalgia|935:squad|936:argument|939:laugh mock|940:temptation|941:begging|942:victory|944:awkward|945:versus
946:backfire|948:lonely_sad|949:fear_panic|950:mock|951:fear_panic|952:lonely_sad|953:smart_idea|955:hard_task|957:fear_panic|958:explain|960:praise_great
964:squad|968:argument|969:confused|970:thinking|971:explain|972:confused|973:fancy|975:money_pay|976:backfire|977:explain|979:explain|983:doom victory
984:begging neglect|985:victory|986:explain|988:begging money_pay|991:reveal|993:choice|995:confused disappointed|997:doom|999:argument|1000:alliance
1003:explain|1005:versus|1007:confused|1009:thinking|1010:then_vs_now|1012:explain|1014:thinking|1015:victory|1017:money_pay|1018:thinking|1020:doom
1022:choice debate|1023:then_vs_now|1024:alliance|1025:explain|1026:levels|1027:secret_smug|1028:power|1030:begging alliance|1031:squad|1034:scream_hype
1035:reaction|1040:reaction|1041:confused|1044:argument|1046:reaction|1047:levels|1048:levels|1049:awkward|1050:levels|1051:thinking|1052:argument
1055:explain|1056:argument protect|1058:money_pay|1059:power|1060:blank levels|1063:praise_great|1065:awkward|1066:argument|1070:backfire|1071:explain
1072:trade_deal|1074:begging argument|1075:disappointed|1076:confused|1078:explain|1079:secret_smug|1080:lonely_sad|1081:rejection|1082:backfire|1084:power
1085:scream_hype|1086:victory|1087:nba_sports confused|1089:loss_regret|1090:smart_idea|1091:explain|1093:reveal|1094:choice|1096:smart_idea|1097:explain
1099:explain|1100:confused|1102:explain|1103:confused|1105:explain|1106:argument|1109:smart_idea|1111:doom|1113:awkward|1115:explain|1116:confused
1117:hard_task|1118:shock lonely_sad|1119:alliance|1123:levels|1124:clown|1125:doom|1126:scream_hype|1127:begging|1128:begging|1129:reaction|1136:begging
1138:praise_great|1140:nba_sports victory|1141:laugh|1144:lonely_sad|1146:lonely_sad|1147:doom|1148:victory|1149:protect|1151:blank|1155:argument
1157:fear_panic reveal|1158:fear_panic|1159:temptation|1160:lonely_sad|1161:fancy|1162:nba_sports laugh|1164:then_vs_now|1165:fancy|1166:clown
1167:secret_smug|1168:streak_fail|1169:awkward|1170:reaction|1171:thinking|1173:fancy|1175:victory|1176:begging|1177:smart_idea|1178:money_pay backfire
1179:versus|1181:argument|1183:doom|1184:loss_regret argument|1185:fear_panic|1186:laugh|1190:explain victory|1193:confused|1195:mock|1196:chaos_evil|1198:explain
"""


def parse():
    out = {}
    for chunk in RAW.replace("\n", "|").split("|"):
        chunk = chunk.strip()
        if ":" in chunk:
            i, cats = chunk.split(":", 1)
            out[int(i)] = cats.split()
    return out
