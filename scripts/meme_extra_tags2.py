"""Second batch of hand tags (ids 1201+) and extra sensitive ids. See extra_tags.py."""
from meme_extra_tags import parse

RAW2 = """
1201:choice|1202:money_pay lonely_sad|1203:protect|1206:confused argument|1208:backfire confused|1209:hard_task|1211:smart_idea|1212:versus same|1216:debate
1217:confused|1220:disappointed|1221:chaos_evil backfire|1225:debate explain|1226:explain|1227:explain|1228:disappointed power|1229:confused|1230:neglect|1231:power
1232:laugh|1234:secret_smug|1239:argument money_pay|1240:lonely_sad|1243:power victory|1244:weak confused|1245:loss_regret|1246:begging|1247:smart_idea|1248:explain
1249:loss_regret|1250:scream_hype|1251:secret_smug|1254:explain|1255:levels|1256:disappointed|1257:streak_fail begging|1258:explain|1259:temptation|1260:alliance
1261:confused|1263:optimist_pessimist|1264:boardroom|1265:lonely_sad|1267:disappointed|1271:levels|1272:fancy|1275:fear_panic|1276:fancy victory|1278:rejection
1280:fear_panic levels|1282:money_pay|1284:mock|1285:boardroom|1287:protect|1289:power|1290:choice|1292:blank|1294:mock|1295:rejection|1296:doom|1297:protect
1298:fear_panic|1299:thinking|1300:disappointed|1302:argument|1303:explain|1307:victory|1308:hard_task|1309:clown|1310:doom|1311:power|1312:reveal|1316:explain
1317:awkward|1318:fear_panic|1321:reveal|1322:explain|1324:secret_smug|1326:nba_sports victory|1327:then_vs_now levels|1330:backfire|1331:explain|1332:mock
1333:shock|1336:explain|1337:victory|1338:streak_fail|1339:scream_hype|1341:confused|1342:fear_panic|1347:then_vs_now|1348:temptation|1349:victory mock
1350:argument versus|1351:mock|1352:temptation|1354:money_pay|1355:thinking|1359:backfire|1360:begging|1361:explain|1363:disappointed|1365:victory|1367:power
1369:rejection|1370:reveal|1373:chaos_evil|1374:reaction|1375:blank|1376:blank|1377:begging|1379:alliance|1380:secret_smug|1382:argument|1383:slap_correct
1387:confused|1389:loss_regret|1390:victory|1391:power|1393:optimist_pessimist|1395:victory|1397:argument|1398:hidden_pain|1399:same|1400:everywhere|1402:alliance
1403:chain_reaction|1404:laugh|1405:doom|1406:reaction|1409:doom power|1410:explain|1411:fear_panic|1412:explain|1414:sleep_bored|1415:disappointed|1417:blank
1418:mock|1420:mock laugh|1421:explain|1422:power|1424:disappointed|1425:nostalgia|1426:choice|1427:fancy|1428:hard_task|1429:power|1430:nostalgia|1432:explain
1433:disappointed|1434:scream_hype|1435:confused|1437:secret_smug|1439:explain|1440:confused|1441:explain|1444:sleep_bored|1447:explain|1448:explain|1449:victory
1450:explain|1451:versus|1454:argument|1455:victory|1456:rejection|1457:reveal|1458:argument|1460:laugh|1461:explain|1462:alliance|1463:praise_great|1464:explain
1465:explain|1466:power|1467:secret_smug|1469:power|1471:chaos_evil|1472:mock|1476:squad|1480:explain|1481:laugh|1482:explain|1484:denial|1486:power|1487:nostalgia
1488:sleep_bored|1491:victory|1495:explain|1496:secret_smug|1498:explain|1499:thinking|1501:reaction|1503:power|1505:same|1506:clown|1507:disappointed|1508:explain
1509:argument|1510:money_pay|1512:secret_smug|1513:reaction|1514:same|1515:explain|1516:argument|1518:victory|1519:smart_idea|1521:explain|1522:mock|1523:explain
1526:victory|1527:argument|1528:fear_panic|1530:backfire|1532:praise_great|1533:power|1535:argument|1536:argument|1538:power|1539:power|1542:mock laugh|1543:disappointed
1547:chaos_evil|1549:clown|1552:fear_panic|1553:blank|1554:victory|1555:chaos_evil|1556:rejection|1558:fancy|1559:hidden_pain|1561:explain|1562:boardroom
1563:smart_idea|1564:explain|1565:praise_great|1566:power|1567:mock|1569:shock|1570:confused|1571:smart_idea|1573:blank|1575:fear_panic|1576:explain|1577:power
1578:doom|1579:mock|1581:fear_panic|1582:explain|1583:laugh|1584:versus alliance|1586:explain|1587:disappointed|1588:disappointed|1589:reveal|1590:confused
1592:blank|1594:money_pay|1595:secret_smug|1597:power|1598:argument|1601:confused|1603:denial|1604:hidden_pain|1605:explain|1607:sleep_bored|1609:versus
1610:disappointed|1611:disappointed|1612:shock|1613:victory|1616:victory|1619:fancy|1622:disappointed|1623:argument|1625:confused|1628:disappointed|1629:disappointed
1630:shock|1633:victory|1635:power|1637:power|1638:shock|1641:secret_smug|1644:argument|1646:reaction|1647:mock|1649:argument|1651:awkward|1652:reaction
1655:rejection|1656:money_pay|1657:lonely_sad|1658:argument|1659:victory|1660:mock|1661:mock|1662:smart_idea|1663:argument|1664:money_pay|1665:explain|1666:shock
1667:boardroom|1668:mock|1669:reveal|1671:awkward|1672:fancy|1674:lonely_sad|1675:argument|1679:confused|1680:confused|1681:mock|1683:mock|1684:mock|1685:secret_smug
1688:versus|1689:explain|1693:lonely_sad|1694:reaction|1695:reaction|1696:argument|1697:fancy|1698:explain|1700:mock|1704:choice|1705:explain|1706:fancy
1709:disappointed|1710:laugh|1711:nostalgia|1712:disappointed|1713:explain|1717:rejection|1718:victory|1719:mock|1721:explain|1722:disappointed
1724:nba_sports argument pointing|1725:awkward|1728:laugh|1730:disappointed|1731:shock|1733:disappointed|1735:laugh|1736:secret_smug|1737:nba_sports argument
1738:victory|1739:awkward|1740:clown|1742:mock|1743:fancy|1744:nba_sports loss_regret|1746:argument|1747:explain|1748:power|1750:explain|1751:disappointed
1752:begging|1754:laugh|1755:fear_panic|1756:confused|1761:reveal|1762:confused|1763:victory|1764:denial|1765:fancy|1768:disappointed|1769:clown|1770:fancy
1772:power clown|1777:confused|1779:confused|1780:nba_sports confused|1783:disappointed|1784:shock|1787:secret_smug|1789:chaos_evil|1793:disappointed
1794:disappointed|1796:confused|1797:begging|1798:fancy|1800:nba_sports reaction|1801:disappointed|1803:nba_sports victory|1804:victory|1806:nba_sports power
1807:disappointed|1808:confused|1810:hidden_pain|1811:fancy|1812:disappointed|1813:blank|1814:explain|1815:mock|1816:explain|1819:nba_sports power|1820:shock
1821:victory|1823:clown|1824:explain|1825:confused|1828:argument|1829:explain|1830:explain|1831:chaos_evil|1837:shock|1838:argument|1839:reaction|1840:lonely_sad
1841:argument|1842:victory|1843:lonely_sad|1845:fancy|1847:disappointed|1848:laugh|1850:reaction|1851:fancy|1853:explain|1854:victory|1855:protect|1856:fancy
1857:sleep_bored|1858:power|1862:secret_smug|1863:argument|1864:explain|1865:victory|1867:explain|1868:mock|1870:confused|1871:awkward|1872:power alliance
1876:scream_hype|1877:hard_task|1880:nba_sports disappointed|1881:power|1883:reaction|1884:smart_idea|1885:argument|1887:victory|1888:power
1890:reaction|1891:mock|1892:mock|1894:protect|1895:awkward
"""

# political figures / stereotypes / drugs / adult / violence -> sensitive (hidden from search)
SENSITIVE_IDS = {1204, 1269, 1371, 1546, 1560, 1596, 1606, 1615, 1618, 1621, 1627, 1636, 1640, 1648, 1653, 1673, 1686,
                 1701, 1702, 1703, 1714, 1716, 1720, 1757, 1759, 1767, 1771, 1778, 1795, 1799, 1802, 1822, 1827, 1832,
                 1833, 1834, 1844, 1846, 1852, 1861, 1866, 1873, 1889, 1037, 1065, 1136, 608, 880}


def parse_all():
    out = parse()
    for chunk in RAW2.replace("\n", "|").split("|"):
        chunk = chunk.strip()
        if ":" in chunk:
            i, cats = chunk.split(":", 1)
            out[int(i)] = cats.split()
    return out
