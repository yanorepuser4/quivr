import Image from "next/image";
import { useEffect, useState } from "react";

import { Sync } from "@/lib/api/sync/types";
import { useSync } from "@/lib/api/sync/useSync";

import styles from "./FromConnections.module.scss";

export const FromConnections = (): JSX.Element => {
  const [userSyncs, setUserSyncs] = useState<Sync[]>([]);
  const { getUserSyncs, iconUrls } = useSync();

  useEffect(() => {
    void (async () => {
      try {
        const res: Sync[] = await getUserSyncs();
        setUserSyncs(res);
      } catch (error) {
        console.error(error);
      }
    })();
  }, []);

  return (
    <div className={styles.user_syncs_wrapper}>
      {userSyncs.map((sync, index) => (
        <div className={styles.user_sync_wrapper} key={index}>
          <Image
            src={iconUrls[sync.provider] || ""}
            alt={sync.name}
            width={24}
            height={24}
          />
          <div>{sync.name}</div>
        </div>
      ))}
    </div>
  );
};